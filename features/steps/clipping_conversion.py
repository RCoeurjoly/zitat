# -*- coding: utf-8 -*-
from behave import given, when, then
from zitat import kindle_clippings_to_org


@given('the kindle generated clipping')
def step_impl(context):
    context.kindle_clipping = context.text


@when('we convert the clipping to org format')
def step_impl(context):  # noqa: F811
    context.org_clipping_result = kindle_clippings_to_org(context.kindle_clipping)


@then('we should get the org clipping')
def step_impl(context):  # noqa: F811
    assert context.org_clipping_result == context.text
