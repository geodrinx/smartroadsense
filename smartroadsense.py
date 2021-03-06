# -*- coding: utf-8 -*-
"""
/***************************************************************************
 smartroadsense
                                 A QGIS plugin
 smartroadsense
                              -------------------
        begin                : 2015-04-14
        git sha              : $Format:%H$
        copyright            : (C) 2015 by geodrinx
        email                : geodrinx@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from smartroadsense_dialog import smartroadsenseDialog
import os.path

from qgis.core import *
from qgis.gui import *
import qgis
from PyQt4.QtCore import QFileInfo
import zipfile 

from qgis.gui import QgsMessageBar

import time
from PyQt4.QtGui import QProgressBar
from PyQt4.QtCore import *

class smartroadsense:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'smartroadsense_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = smartroadsenseDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&smartroadsense')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'smartroadsense')
        self.toolbar.setObjectName(u'smartroadsense')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('smartroadsense', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/smartroadsense/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'SmartRoadSense'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&smartroadsense'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

#  hhttp://smartroadsense.it/data/srs_data.zip
#  hhttp://smartroadsense.it/open_data.zip

    def run(self):
    
            import urllib2    
    
            stringa1 = "http://smartroadsense.it/open_data.zip"
        
            mapCanvas = self.iface.mapCanvas()

#--------------------------------
            progressMessageBar = self.iface.messageBar().createMessage("SmartRoadSense: Loading remote CSV Open Data.  Please, wait...")
            progress = QProgressBar()

            progress.setMaximum(10)
            progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            progressMessageBar.layout().addWidget(progress)

            self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)
            
            for i in range(10):
                  time.sleep(1)
                  progress.setValue(i + 1)
            self.iface.messageBar().clearWidgets()            
#--------------------------------

            msg = ("Loading remote csv open data.  Please, wait...")
            self.iface.messageBar().pushMessage("SmartRoadSense:   ",
                                                msg,
                                                QgsMessageBar.INFO, 3)


            tempDir = unicode(QFileInfo(QgsApplication.qgisUserDbFilePath()).path()) + "/python/plugins/smartroadsense/temp/"
            
            stringaUrl = stringa1
 
            try:                   
               response = urllib2.urlopen(stringaUrl)
               print "downloading " + stringaUrl
               
               Zippo = response.read()

            except HTTPError, e:
               print "HTTP Error:",e.code , url
            except URLError, e:
               print "URL Error:",e.reason , url



            nomeZIP = tempDir + "open_data.zip"
            nomeZIP.replace("\\", "/")
            nomeZIP.replace("//", "/") 
#            print ("%s\n") %(nomeZIP)
                   
            f = open(nomeZIP, 'wb')				
            f.write(Zippo)
            f.close()


            zip = zipfile.ZipFile(nomeZIP)  
            zip.extractall(tempDir)  

            nomecsv = tempDir + "open_data.csv"
            nomecsv.replace("\\", "/") 
            uri = """file:///""" + nomecsv + """?"""
            uri += """type=csv&"""
#            uri += """delimiter=,&"""
#            uri += """trimFields=Yes&"""
            uri += """trimFields=no&"""
            uri += """xField=LONGITUDE&"""
            uri += """yField=LATITUDE&"""
            uri += """spatialIndex=yes&"""
            uri += """subsetIndex=no&"""
            uri += """watchFile=no&"""
            uri += """crs=epsg:4326"""

                       
            vlayer = QgsVectorLayer(uri, "SmartRoadSense", "delimitedtext")


            for iLayer in range(mapCanvas.layerCount()):
               layer = mapCanvas.layer(iLayer)
               if layer.name() == "SmartRoadSense":
                  QgsMapLayerRegistry.instance().removeMapLayer(layer.id())                  

        
            QgsMapLayerRegistry.instance().addMapLayer(vlayer)   


            nomeqml = tempDir + "open_data.qml"            
            nomeqml.replace("\\", "/")


            result = vlayer.loadNamedStyle(nomeqml)            
#            if (result == False ):
#               print("error loading QML !\n")
                                             
            vlayer.triggerRepaint()
            
            mapCanvas.refresh()            
