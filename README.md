panda3d-editor
==============

A simple, lightweight editor for the Panda3D engine. 

Features include:

* Ability to add lights and models to a scene 
* Gizmos to allow easy transformation of nodes
* Ability to edit node properties
* Node duplication
* Undo / redo
* Project management, including ablity to build a project to a p3d multifile
* Save / restore scene in xml format
* Support for user created plugins

## Usage

To give the editor a spin, try the following:

* Create a new project
* Import some models (.egg or .bam)
* Middle mouse drag them into the scene
* Translate, rotate and scale them as your desire
* Set up some lights with the Create menu
* Save the scene as test.xml
* Build your project (File -> Build)
You should now have a p3d file which runs your scene. 
 
## Keys

* 4 - Wireframe view
* 5 - Shaded view
* 6 - Textured view
* Q - Select
* W - Translate
* E - Rotate
* R - Scale
* Z - Undo
* Shift-Z - Redo
* F - Frame selection
* Backspace - Delete
* Ctrl-D - Duplicate
* Arrow up - Select parent
* Arrow down - Select child
* Arrow left - Select previous child
* Arrow right - Select next child
* Mouse left - Pointing and selecting
* Middle mouse - Your "doing" button. Use then to reparent nodes in the scene graph, or drag-drop models into the scene. 

## Requires

* Panda3D
* wxPython