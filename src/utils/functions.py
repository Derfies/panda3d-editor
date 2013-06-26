import threading
import subprocess


def Indent( elem, level=0, indent='    ' ):
    """
    Function used to 'prettify' output xml from cElementTree's tree.getroot() 
    method into lines so it's easily read.
    """
    i = "\n" + level * indent
    if len( elem ):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            Indent( elem, level + 1, indent )
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and ( not elem.tail or not elem.tail.strip() ):
            elem.tail = i
            

def GetCamelCase( name ):
    return name[0].upper() + name[1:]
            

def GetLowerCamelCase( name ):
    return name[0].lower() + name[1:]
    

def GetUniqueName( name, elems ):
    """
    Return a unique version of the name indicated by incrementing a numeral
    at the end. Stop when the name no longer appears in the indicated list of
    elements.
    """
    digits = []
    for c in reversed( name ):
        if c.isdigit():
            digits.append( c )
        else:
            break
   
    stem = name[0:len( name ) - len( digits )]
    val = ''.join( digits )[::-1] or 0
    i = int( val )
        
    while True:
        i += 1
        newName = ''.join( [stem, str( i )] )
        if newName not in elems:
            break
        
    return newName
    

def PopenAndCall( OnExit, printStdout, *popenArgs, **popenKWArgs ):
    """
    Runs a subprocess.Popen, and then calls the function onExit when the
    subprocess completes.

    Use it exactly the way you'd normally use subprocess.Popen, except include 
    q callable to execute as the first argument. onExit is a callable object, 
    and *popenArgs and **popenKWArgs are simply passed up to subprocess.Popen.
    """
    def RunInThread( OnExit, printStdout, popenArgs, popenKWArgs ):
        proc = subprocess.Popen( *popenArgs, **popenKWArgs )
        proc.wait()
        if printStdout:
            print proc.stdout.read()
        OnExit()
        return

    thread = threading.Thread( target=RunInThread,
                               args=( OnExit, printStdout, popenArgs, 
                                      popenKWArgs ) )
    thread.start()
    
    # Return immediately after the thread starts.
    return thread 