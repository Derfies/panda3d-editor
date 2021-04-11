import threading
import subprocess


def indent(elem, level=0, indent='    '):
    """
    Function used to 'prettify' output xml from cElementTree's tree.getroot() 
    method into lines so it's easily read.

    """
    i = "\n" + level * indent
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1, indent)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def popen_and_call(OnExit, printStdout, *popenArgs, **popenKWArgs):
    """
    Runs a subprocess.Popen, and then calls the function onExit when the
    subprocess completes.

    Use it exactly the way you'd normally use subprocess.Popen, except include 
    q callable to execute as the first argument. onExit is a callable object, 
    and *popenArgs and **popenKWArgs are simply passed up to subprocess.Popen.

    """
    def run_in_thread(OnExit, printStdout, popenArgs, popenKWArgs):
        proc = subprocess.Popen(*popenArgs, **popenKWArgs)
        proc.wait()
        if printStdout:
            print(proc.stdout.read())
        OnExit()
        return

    thread = threading.Thread(
        target=run_in_thread,
        args=(
            OnExit,
            printStdout,
            popenArgs,
            popenKWArgs
        )
    )
    thread.start()
    
    # Return immediately after the thread starts.
    return thread
