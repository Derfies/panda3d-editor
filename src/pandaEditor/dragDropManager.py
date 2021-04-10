import os

import wx

import commands as cmds


class DragDropManager:
    
    def __init__(self, app):
        self.app = app
        self.dragComps = []
        
        # Define file types and their actions.
        self.fileTypes = {
            '.egg': self.AddModel,
            '.bam': self.AddModel,
            '.pz': self.AddModel,
            '.sha': self.AddShader#,
            #'.png':self.app.AddTexture,
            #'.tga':self.app.AddTexture,
            #'.jpg':self.app.AddTexture
        }
        
    def DoFileDrop(self, filePath, np):
        ext = os.path.splitext(filePath)[1]
        if ext in self.fileTypes:
            fn = self.fileTypes[ext]
            fn(filePath, np)
        
    def Start(self, src, dragComps, data):
        self.dragComps = dragComps
        
        # Create a custom data object that we can drop onto the toolbar
        # which contains the tool's id as a string
        do = wx.CustomDataObject('NodePath')
        #do = wx.TextDataObject('NodePath')
        # print('data:', data)
        # print('str data:', str( data ))
        import pickle
        data = pickle.dumps(data)
        do.SetData( data )
        #do.SetText(data)
        
        # Create the drop source and begin the drag and drop operation
        ds = wx.DropSource( src )
        ds.SetData( do )
        ds.DoDragDrop(True)# wx.Drag_AllowMove )
        
        # Clear drag node paths
        self.dragComps = []
        
    def ValidateDropItem( self, x, y, parent ):
        dropComp = parent.GetDroppedObject( x, y )
        #if dropComp is None:
        if len( self.dragComps ) == 1:
            try:
                filePath = self.dragComps[0]
                ext = os.path.splitext( filePath )[1]
                #print 'in: ',  ext in self.fileTypes
                return ext in self.fileTypes
            except Exception:
                pass
                #print e
                #return False
        #return False
        
        wrpr = base.game.nodeMgr.Wrap( dropComp )
        if wx.GetMouseState().CmdDown():
            return wrpr.ValidateDragDrop( self.dragComps, dropComp )
        else:
            return wrpr.GetPossibleConnections( self.dragComps )
            
    def OnDropItem( self, str, parent, x, y ):
        
        # Get the item at the drop point
        dropComp = parent.GetDroppedObject( x, y )
        if len( self.dragComps ) == 1:
            try:
                filePath = self.dragComps[0]
                self.DoFileDrop( filePath, dropComp )
            except:
                pass
        if dropComp is None:
            return
        wrpr = base.game.nodeMgr.Wrap( dropComp )
        self.data = {}
        dragComps = self.app.dDropMgr.dragComps
        if wx.GetMouseState().CmdDown():
            wrpr.OnDragDrop( dragComps, wrpr.data )
        else:
            menu = wx.Menu()
            for cnnctn in wrpr.GetPossibleConnections( dragComps ):
                mItem = wx.MenuItem( menu, wx.NewId(), cnnctn.label )
                menu.AppendItem( mItem )
                menu.Bind( wx.EVT_MENU, self.OnConnect, id=mItem.GetId() )
                self.data[mItem.GetId()] = cnnctn
            parent.PopupMenu( menu )
            menu.Destroy()
        
    def OnConnect( self, evt ):
        dragComps = self.app.dDropMgr.dragComps
        menu = evt.GetEventObject()
        mItem = menu.FindItemById( evt.GetId() )
        cnnctn = self.data[evt.GetId()]
        cmds.Connect( dragComps, cnnctn, cnnctn.Connect )
            
    def AddModel(self, filePath, np=None):
        self.app.AddComponent('ModelRoot', modelPath=filePath)
        
    def AddShader( self, filePath, np=None ):
        wrpr = base.game.nodeMgr.Wrap( np )
        prop = wrpr.FindProperty( 'shader' )
        cmds.SetAttribute( [np], [prop], filePath )
        
    def AddTexture( self, filePath, np=None ):
        pandaPath = pm.Filename.fromOsSpecific( filePath )
        
        theTex = None
        if pm.TexturePool.hasTexture( pandaPath ):
            print('found in pool')
            for tex in pm.TexturePool.findAllTextures():
                if tex.getFilename() == pandaPath:
                    theTex = tex
        
        # Try to find it in the scene.
        #for foo in base.scene.comps.keys():
        #    print type( foo ) , ' : ', foo
        print(theTex)
        if theTex is not None and theTex in base.scene.comps.keys():
            print('found in scene')
            if np is not None:
                npWrpr = base.game.nodeMgr.Wrap( np )
                npWrpr.FindProperty( 'texture' ).Set( theTex )
                
        else:
            
            print('creating new')
            wrpr = self.AddComponent( 'Texture' )
            #wrpr = base.game.nodeMgr.Wrap( loader.loadTexture( pandaPath ) )
            #wrpr.SetDefaultValues()
            #wrpr.SetParent( wrpr.GetDefaultParent() )
            wrpr.FindProperty( 'fullPath' ).Set( pandaPath )
            #pm.TexturePool.addTexture( wrpr.data )
            
            if np is not None:
                npWrpr = base.game.nodeMgr.Wrap( np )
                npWrpr.FindProperty( 'texture' ).Set( wrpr.data )
            
            
            #cmds.Connect( 