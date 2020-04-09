# -*- coding: utf-8 -*-
import os
import sys
from behave import *
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "../../zitat.py")
from zitat import *

@given('the kindle generated clipping')
def step_impl(context):
    context.kindle_clipping = context.text

@when('we convert the clipping to org format')
def step_impl(context):
    context.org_clipping_result = kindle_clippings_to_org(context.kindle_clipping)

@then('we should get the org clipping')
def step_impl(context):
    # print("Input:\n" + context.kindle_clipping)
    # print("Expected result:\n" + context.text)
    # with open("expected.txt","w") as expected:
    #     expected.write(context.text)
    # print("Actual result:\n" + context.org_clipping_result)
    # with open("actual.txt","w") as actual:
    #     actual.write(context.org_clipping_result)
    assert context.org_clipping_result == context.text
