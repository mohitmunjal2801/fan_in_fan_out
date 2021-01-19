import pathlib
import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):

    root_directory: str = context.get_input()

    if not root_directory:
        raise Exception("A directory path is required as input")

    #files = yield context.call_activity("E2_GetFileList", root_directory)
    files = root_directory.split(',')
    upload_tasks = []
    getfile_tasks = []
    input_files = []
    output_files = []
    for file in files:
        upload_tasks.append(context.call_activity("E2_CopyFileToBlob", file))
    input_files = yield context.task_all(upload_tasks)
    #input_files.append(input_file)
    for fileItem in input_files:
      fname = pathlib.Path(fileItem).parts[-1:]
      getfile_tasks.append(context.call_activity("E2_GetFileList", fname[0]))
    output_files = yield context.task_all(getfile_tasks)
    #output_files.append(output_file)
    return output_files

main = df.Orchestrator.create(orchestrator_function)