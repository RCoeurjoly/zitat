# -*- coding: utf-8 -*-
import os
import sys
from behave import *
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "../../zitat.py")
from zitat import *
import re

@given('the kindle timestamp "{kindle_timestamp}"')
def step_impl(context, kindle_timestamp):
    context.kindle_timestamp = kindle_timestamp

@when('we convert the English timestamp to org format')
def step_impl(context):
    context.expected_org_timestamp = EN_kindle_timestamp_to_ISO_8601(context.kindle_timestamp)

@when('we convert the Chinese timestamp to org format')
def step_impl(context):
    context.expected_org_timestamp = ZH_kindle_timestamp_to_ISO_8601(context.kindle_timestamp)

@then('we should have the org timestamp "{org_timestamp}"')
def step_impl(context, org_timestamp):
    assert context.expected_org_timestamp == org_timestamp
