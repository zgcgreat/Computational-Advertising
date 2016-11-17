/** creative_filters.cc                                 -*- C++ -*-
    Rémi Attab, 09 Aug 2013
    Copyright (c) 2013 Datacratic.  All rights reserved.

    Registry and implementation of the creative filters.

*/

#include "creative_filters.h"

using namespace std;
using namespace ML;

namespace RTBKIT {


/******************************************************************************/
/* CREATIVE SEGMENTS FILTER                                                   */
/******************************************************************************/

void
CreativeSegmentsFilter::
filter(FilterState& state) const
{
    unordered_set<string> toCheck = excludeIfNotPresent;

    for (const auto& segment : state.request.segments) {
        toCheck.erase(segment.first);

        auto it = data.find(segment.first);
        if (it == data.end()) continue;

        CreativeMatrix result = it->second.ie.filter(*segment.second);
        state.narrowAllCreatives(result);

        if (state.configs().empty()) return;
    }

    for (const auto& segment : toCheck) {
        auto it = data.find(segment);
        if (it == data.end()) continue;

        CreativeMatrix result = it->second.excludeIfNotPresent.negate();
        state.narrowAllCreatives(result);
        if (state.configs().empty()) return;
    }
}

void
CreativeSegmentsFilter::
setCreative(unsigned configIndex, unsigned crIndex, const Creative& creative, bool value)
{
    for (const auto& entry : creative.segments) {
        auto& segment = data[entry.first];

        segment.ie.setInclude(configIndex, crIndex, value, entry.second.include);
        segment.ie.setExclude(configIndex, crIndex, value, entry.second.exclude);

        if (entry.second.excludeIfNotPresent) {
            if (value && segment.excludeIfNotPresent.empty())
                excludeIfNotPresent.insert(entry.first);

            segment.excludeIfNotPresent.set(crIndex, configIndex, value);

            if (!value && segment.excludeIfNotPresent.empty())
                excludeIfNotPresent.erase(entry.first);
        }
    }
}

/******************************************************************************/
/* INIT FILTERS                                                               */
/******************************************************************************/

namespace {

struct AtInit {
    AtInit()
    {
        RTBKIT::FilterBase::registerFactory<RTBKIT::CreativeFormatFilter>();
        RTBKIT::FilterBase::registerFactory<RTBKIT::CreativeLanguageFilter>();
        RTBKIT::FilterBase::registerFactory<RTBKIT::CreativeLocationFilter>();

        RTBKIT::FilterBase::registerFactory<RTBKIT::CreativeExchangeNameFilter>();
        RTBKIT::FilterBase::registerFactory<RTBKIT::CreativeExchangeFilter>();
        RTBKIT::FilterBase::registerFactory<RTBKIT::CreativeSegmentsFilter>();
        RTBKIT::FilterBase::registerFactory<RTBKIT::CreativePMPFilter>();
    }

} AtInit;

} // namespace anonymous

} // namepsace RTBKIT
