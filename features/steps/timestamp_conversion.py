# -*- coding: utf-8 -*-
from hamcrest import assert_that, equal_to
from behave import given, when, then
from zitat import EN_kindle_timestamp_to_ISO_8601, ZH_kindle_timestamp_to_ISO_8601, kindle_timestamp_to_ISO_8601


@given('the kindle timestamp "{kindle_timestamp}"')
def step_impl(context, kindle_timestamp):
    context.kindle_timestamp = kindle_timestamp


@when('we convert the English timestamp to org format')
def step_impl(context):  # noqa: F811
    context.expected_org_timestamp = EN_kindle_timestamp_to_ISO_8601(context.kindle_timestamp)


@when('we convert the Chinese timestamp to org format')
def step_impl(context):  # noqa: F811
    context.expected_org_timestamp = ZH_kindle_timestamp_to_ISO_8601(context.kindle_timestamp)


@when('we convert the timestamp to org format')
def step_impl(context):  # noqa: F811
    context.expected_org_timestamp = kindle_timestamp_to_ISO_8601(context.kindle_timestamp)


@then('we should have the org timestamp "{org_timestamp}"')
def step_impl(context, org_timestamp):  # noqa: F811
    assert_that(context.expected_org_timestamp, equal_to(org_timestamp))
