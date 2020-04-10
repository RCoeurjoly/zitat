# -*- coding: utf-8 -*-
from hamcrest import assert_that, equal_to
from behave import given, when, then
from zitat import kindle_clippings_to_org, zitat


@given('the kindle generated clipping')
def step_impl(context):
    context.kindle_clipping = context.text


@given('the kindle generated clipping file "{filename}" whose content is')
def step_impl(context, filename):  # noqa: F811
    context.input_file = "features/temp/" + filename
    with open(context.input_file, 'w', encoding='utf-8') as in_file:
        in_file.write(context.text)


@when('we convert the input file to the org file "{filename}"')
def step_impl(context, filename):  # noqa: F811
    context.output_file = "features/temp/" + filename
    my_args = ['', context.input_file, context.output_file]
    print(my_args)
    zitat(my_args)


@when('we convert the clipping to org format')
def step_impl(context):  # noqa: F811
    context.org_clipping_result = kindle_clippings_to_org(context.kindle_clipping)


@then('we should get the org clipping')
def step_impl(context):  # noqa: F811
    assert_that(context.org_clipping_result, equal_to(context.text))


@then('we should get an org file whose content is')
def step_impl(context):  # noqa: F811
    with open(context.output_file, 'r', encoding='utf-8') as out_file:
        output_file_as_string = out_file.read()
    assert_that(output_file_as_string, equal_to(context.text))
