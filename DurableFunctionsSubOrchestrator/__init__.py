# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    upload_tasks = []
    input_files = []
    filesStr:str = context.get_input()
    files = filesStr.split(',')
    for file in files:
        upload_tasks.append(context.call_activity("E2_CopyFileToBlob", file))
    input_files = yield context.task_all(upload_tasks)
   
    return input_files

main = df.Orchestrator.create(orchestrator_function)