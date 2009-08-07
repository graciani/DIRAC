# $Header: /tmp/libdirac/tmp.stZoy15380/dirac/DIRAC3/DIRAC/FrameworkSystem/Service/PlottingHandler.py,v 1.3 2009/08/07 13:06:32 atsareg Exp $

""" Plotting Service generates graphs according to the client specifications
    and data
"""

__RCSID__ = "$Id: PlottingHandler.py,v 1.3 2009/08/07 13:06:32 atsareg Exp $"

from types import *
import os
import md5
from DIRAC import S_OK, S_ERROR, rootPath, gConfig, gLogger, gMonitor
from DIRAC.ConfigurationSystem.Client import PathFinder
from DIRAC.Core.Utilities import Time
from DIRAC.Core.DISET.RequestHandler import RequestHandler
from DIRAC.FrameworkSystem.Service.PlotCache import gPlotCache
from DIRAC.Core.Utilities.Graphs import graph
import tempfile 

def initializePlottingHandler( serviceInfo ):

  #Get data location
  plottingSection = PathFinder.getServiceSection( "Framework/Plotting" )
  dataPath = gConfig.getValue( "%s/DataLocation" % plottingSection, "data/graphs" )  
  dataPath = dataPath.strip()
  if "/" != dataPath[0]:
    dataPath = os.path.realpath( "%s/%s" % ( rootPath, dataPath ) )
  gLogger.info( "Data will be written into %s" % dataPath )
  try:
    os.makedirs( dataPath )
  except:
    pass
  try:
    testFile = "%s/plot__.test" % dataPath
    fd = file( testFile, "w" )
    fd.close()
    os.unlink( testFile )
  except IOError:
    gLogger.fatal( "Can't write to %s" % dataPath )
    return S_ERROR( "Data location is not writable" )
    
  gPlotCache.setPlotsLocation( dataPath )
  gMonitor.registerActivity( "plotsDrawn", "Drawn plot images", "Plotting requests", "plots", gMonitor.OP_SUM )
  return S_OK()

class PlottingHandler( RequestHandler ):
    
  def __calculatePlotHash(self,data,metadata,subplotMetadata):
    m = md5.new()
    m.update(repr({'Data':data,'PlotMetadata':metadata,'SubplotMetadata':subplotMetadata}))
    return m.hexdigest()  
    
  types_generatePlot = [ [DictType,ListType], DictType, [DictType,ListType] ]
  def export_generatePlot( self, data, plotMetadata, subplotMetadata ):
    """ Create a plot according to the client specification and return its name
    """

    plotHash = self.__calculatePlotHash(data,plotMetadata,subplotMetadata)
    result = gPlotCache.getPlot(plotHash,data,plotMetadata,subplotMetadata)
    if not result['OK']:
      return result
    return S_OK(result['Value']['plot'])    

  def transfer_toClient( self, fileId, token, fileHelper ):
    """
    Get graphs data
    """
    retVal = gPlotCache.getPlotData( fileId )
    if not retVal[ 'OK' ]:
      return retVal
    retVal = fileHelper.sendData( retVal[ 'Value' ] )
    if not retVal[ 'OK' ]:
      return retVal
    fileHelper.sendEOF()
    return S_OK()
