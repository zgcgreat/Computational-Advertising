# exchange_testing.mk

#$(eval $(call test,rubicon_exchange_connector_test,rubicon_exchange bid_test_utils openrtb_exchange bidding_agent rtb_router cairomm-1.0 cairo sigc-2.0,boost))
$(eval $(call test,mopub_exchange_connector_test,mopub_exchange bid_test_utils openrtb_exchange bidding_agent rtb_router sigc-2.0,boost manual))
$(eval $(call test,smaato_exchange_connector_test,smaato_exchange bid_test_utils openrtb_exchange bidding_agent rtb_router sigc-2.0,boost))
$(eval $(call test,gumgum_exchange_connector_test,gumgum_exchange bid_test_utils openrtb_bid_request bidding_agent rtb_router agents_bidder,boost))
$(eval $(call test,bidswitch_exchange_connector_test,bidswitch_exchange bid_test_utils bidding_agent rtb_router agents_bidder,boost))
$(eval $(call test,bidswitch_exchange_connector_adx_test,bidswitch_exchange bid_test_utils bidding_agent rtb_router agents_bidder,boost))
$(eval $(call test,bidswitch_filters_test,static_filters bidswitch_exchange,boost))
$(eval $(call test,nexage_exchange_connector_test,nexage_exchange bid_test_utils bidding_agent rtb_router agents_bidder,boost))
$(eval $(call test,adx_exchange_connector_test,adx_exchange bid_test_utils bidding_agent rtb_router agents_bidder,boost))
$(eval $(call test,openrtb_exchange_connector_test,openrtb_exchange bid_test_utils bidding_agent rtb_router agents_bidder,boost))
$(eval $(call test,rtbkit_exchange_connector_test,rtbkit_exchange bid_test_utils bidding_agent rtb_router agents_bidder,boost))
$(eval $(call test,casale_exchange_connector_test,casale_exchange bid_test_utils bidding_agent rtb_router agents_bidder,boost))
$(eval $(call test,creative_ids_exchange_filter_test,static_filters rtbkit_exchange,boost))
$(eval $(call test,spotx_exchange_connector_test,spotx_exchange bid_test_utils bidding_agent rtb_router agents_bidder,boost))

$(eval $(call test,creative_configuration_test,exchange agent_configuration bid_request jsoncpp types,boost))
