/* creative_configuration.h                           -*- C++ -*-
   Thomas Sanchez, 18 October 2013
   Copyright (c) 2013 mbr targeting GmbH.  All rights reserved.
*/

#pragma once

#include <initializer_list>
#include <string>
#include <vector>
#include <map>

#include <boost/thread.hpp>

#include "rtbkit/common/exchange_connector.h"
#include "rtbkit/common/auction.h"
#include "rtbkit/common/expand_variable.h"
#include "rtbkit/common/creative_field.h"

namespace RTBKIT {

class CreativeConfiguration
{
public:
    struct Context {
        const Creative& creative;
        const Auction::Response& response;
        const BidRequest& bidrequest;
        int spotNum;
    };

    enum class Verbosity { Verbose, Quiet };

    typedef std::function<std::string &(std::string &)> ExpanderFilterCallable;
    typedef std::map<std::string, ExpanderFilterCallable> ExpanderFilterMap;
    typedef std::function<std::string(const Context &)> ExpanderCallable;
    typedef std::map<std::string, ExpanderCallable> ExpanderMap;


    CreativeConfiguration(const std::string& exchange);

    virtual RTBKIT::ExchangeConnector::ExchangeCompatibility
    handleCreativeCompatibility(const Creative& creative,
                                const bool includeReasons,
                                Verbosity verbosity = Verbosity::Quiet) const = 0;

    virtual std::string expand(const std::string& templateString,
                       const Context& context) const = 0;

    void addExpanderVariable(const std::string& key, ExpanderCallable value)
    {
        expanderDict_[key] = value;
    }

    void addExpanderFilter(const std::string& filter,
                           ExpanderFilterCallable callable)
    {
        filters_[filter] = callable;
    }

    std::string exchange() const { return exchange_; }

private:
    void registerDefaultExpanders();
    void registerDefaultFilters();
    void registerCustomExpanders();

protected:
    const std::string exchange_;

    ExpanderMap expanderDict_;
    ExpanderFilterMap filters_;
};

template <typename CreativeData>
class TypedCreativeConfiguration : public CreativeConfiguration
{
public:
    static const std::string VARIABLE_MARKER_BEGIN;
    static const std::string VARIABLE_MARKER_END;

    typedef CreativeField<CreativeData> Field;

    struct Expander;

    TypedCreativeConfiguration(const std::string& exchange)
        : CreativeConfiguration(exchange)
    { }

    Field & addField(const std::string & name,
                     typename Field::Handler handler)
    {
        return fields_[name] = Field(name, handler);
    }

    RTBKIT::ExchangeConnector::ExchangeCompatibility
    handleCreativeCompatibility(const Creative& creative,
                                const bool includeReasons,
                                Verbosity verbosity = Verbosity::Quiet) const;

    std::string expand(const std::string& templateString,
                       const Context& context) const;

private:
    std::vector<ExpandVariable>
    extractVariables(const std::string& snippet) const;

    Expander
    generateExpander(const std::vector<ExpandVariable>& variables) const;

    ExpanderCallable getAssociatedCallable(ExpandVariable const& var) const;
    std::string jsonValueToStr(Json::Value const& val) const;

    /**
     * The map is mutable because it is populated in the
     * getCreativeCompatibility and this member function is required to be
     * const
     */
    mutable std::unordered_map<std::string, Expander> expanders_;
    mutable boost::shared_mutex mutex_;

    std::map<std::string, Field> fields_;
};

template<typename CreativeData>
const std::string TypedCreativeConfiguration<CreativeData>::VARIABLE_MARKER_BEGIN = "%{";

template<typename CreativeData>
const std::string TypedCreativeConfiguration<CreativeData>::VARIABLE_MARKER_END = "}";

template<typename CreativeData>
struct TypedCreativeConfiguration<CreativeData>::Expander
{
    typedef std::vector<std::pair<ExpandVariable, ExpanderCallable>> FunctorCollection;

    void addFunctor(const ExpandVariable& var, ExpanderCallable fn)
    {
        collection.push_back(std::make_pair(var, fn));
    }

    void finalize()
    {
        std::reverse(collection.begin(), collection.end());
    }

    std::string expand(std::string toExpand, const Context& ctx) const
    {
        for (auto& element : collection) {
            auto const& var = element.first;
            auto const& fn = element.second;

            auto const& location = var.getReplaceLocation();

            toExpand.replace(
                location.first, location.second - location.first, fn(ctx));
        }

        return toExpand;
    }

    FunctorCollection collection;

};



template <typename CreativeData>
RTBKIT::ExchangeConnector::ExchangeCompatibility
TypedCreativeConfiguration<CreativeData>::handleCreativeCompatibility(
    const Creative& creative, const bool includeReasons, Verbosity verbosity) const
{

    RTBKIT::ExchangeConnector::ExchangeCompatibility result;
    result.setCompatible();

    auto const& config = creative.providerConfig[exchange_];

    if (config == Json::Value::null) {
        result.setIncompatible("No configuration for exchange: " + exchange_,
                               includeReasons);
        return result;
    }

    auto data = std::make_shared<CreativeData>();

    for (const auto & pair : fields_) {
        const auto & field = pair.second;
        auto value = field.extractJsonValue(config);

        if (value.isNull()) {
            std::ostringstream oss;
            oss << "test" << ": " << creative.name << " does not have the "
                << (field.isRequired() ? "required" : "optional")
                << " configuration variable '" << field.getName() << "'";

            if (field.isRequired()) {
                result.setIncompatible(oss.str(), includeReasons);
                return result;
            } else if (verbosity == Verbosity::Verbose) {
                std::cerr << oss.str() << std::endl;
            }

        } else {
            try {
                if (!field(value, *data)) {
                    result.setIncompatible(
                        exchange_ + ": " + creative.name + ": value: " +
                            value.toString() +
                            " was not handled properly by the connector.",
                        includeReasons);
                    return result;
                }
            }
            catch (const std::exception & exc)
            {
                result.setIncompatible(exchange_ + ": " + creative.name +
                                           ": value: " + value.toString() +
                                           " was not handled properly by the "
                                           "connector, exception:" +
                                           exc.what(),
                                       includeReasons);
                return result;
            }

            if (field.isSnippet()) {
                // assume string
                auto const& snippet = value.asString();
                auto expander = generateExpander(extractVariables(snippet));
                boost::unique_lock<boost::shared_mutex> lock(mutex_);
                expanders_[snippet] = expander;
            }
        }
    }

    result.info = data;
    return result;
}

template <typename CreativeData>
std::vector<ExpandVariable>
TypedCreativeConfiguration<CreativeData>::extractVariables(
    const std::string& snippet) const
{
    std::vector<ExpandVariable> variables;

    for (auto index = snippet.find(VARIABLE_MARKER_BEGIN), indexEnd = size_t(0);
         index != std::string::npos;
         index = snippet.find(VARIABLE_MARKER_BEGIN, indexEnd)) {

        auto vBegin = index + VARIABLE_MARKER_BEGIN.size();
        indexEnd = snippet.find(VARIABLE_MARKER_END, vBegin);
        if (indexEnd == std::string::npos) {
            throw std::invalid_argument(exchange_ + ": starting at pos " +
                                        std::to_string(vBegin) + ", " +
                                        VARIABLE_MARKER_END + " is expected");
        }

        auto variable = snippet.substr(vBegin, indexEnd - vBegin);
        indexEnd += VARIABLE_MARKER_END.size();
        variables.emplace_back(variable, index, indexEnd);
    }

    return std::move(variables);
}

template <typename CreativeData>
CreativeConfiguration::ExpanderCallable
TypedCreativeConfiguration<CreativeData>::getAssociatedCallable(
    ExpandVariable const& var) const
{
    auto it = expanderDict_.find(var.getVariable());
    if (it != expanderDict_.end()) {
        return it->second;
    }

    auto const& path = var.getPath();
    auto const& section = path[0];

    auto getter = [this, var](Json::Value const & jsonVal,
                              const Context & context)->std::string
    {

        auto const& path = var.getPath();
        auto val = jsonVal;
        for (auto it = std::begin(path) + 1, end = std::end(path);
             val != Json::Value::null && it != end;
             ++it) {
            val = val[*it];
        }

        if (val != Json::Value::null) {
            return this->jsonValueToStr(val);
        }

        return "";
    };

    if (section == "creative") {
        return [getter](const Context & context) {
            return getter(context.creative.toJson(), context);
        };
    } else if (section == "bidrequest") {
        return [getter](const Context & context) {
            return getter(context.bidrequest.toJson(), context);
        };
    } else if (section == "meta") {
        return [this, getter](const Context & context) {
            Json::Reader reader;
            Json::Value val;
            if (!reader.parse(context.response.meta.rawString(), val)) {
                std::cerr << "Failed to parse meta information for exchange:"
                          << this->exchange_
                          << ", meta: " << context.response.meta << std::endl;
            }

            return getter(val, context);
        };
    }

    throw std::runtime_error("Invalid variable: " + var.getVariable());
}


template <typename CreativeData>
typename TypedCreativeConfiguration<CreativeData>::Expander
TypedCreativeConfiguration<CreativeData>::generateExpander(
    const std::vector<ExpandVariable>& variables) const
{
    Expander expander;
    for (auto const& variable : variables) {
        auto callable = getAssociatedCallable(variable);

        ExpanderFilterCallable filterFn;

        auto const& filters = variable.getFilters();
        for (auto const& filter : filters) {
            auto it = filters_.find(filter);
            if (it == filters_.end()) {
                throw std::runtime_error("Invalid filter: " + filter);
            }

            auto currentFilter = it->second;
            if (filterFn) {
                filterFn = [currentFilter, filterFn](std::string& value)
                    -> std::string&
                {
                    return currentFilter(filterFn(value));
                };
            } else {
                filterFn = currentFilter;
            }
        }

        if (filterFn) {

            expander.addFunctor(
                    variable,
                    [filterFn, callable](Context const & ctx) {
                        std::string result = callable(ctx);
                        filterFn(result);
                        return result;
            });
        } else {
            expander.addFunctor(variable, callable);
        }
    }

    expander.finalize();
    return expander;
}

template <typename CreativeData>
std::string
TypedCreativeConfiguration<CreativeData>::jsonValueToStr(
    Json::Value const& val) const
{
    if (val.isUInt()) {
        return std::to_string(val.asUInt());
    }

    if (val.isIntegral()) {
        return std::to_string(val.asInt());
    }

    if (val.isString()) {
        return val.asString();
    }

    std::cerr << exchange_ << ": Cannot convert json value : " << val.toString()
              << " to string. Actual type: " << val.type() << " not supported"
              << std::endl;

    return "";
}

template <typename CreativeData>
std::string
TypedCreativeConfiguration<CreativeData>::expand(const std::string& templateString,
                                            const Context& context) const
{
    boost::shared_lock<boost::shared_mutex> lock(mutex_);
    auto const& expander = expanders_[templateString];
    return expander.expand(templateString, context);
}


} // namespace RTBKIT
