
///@file Helper.hpp Helper functions.

//============================================================================
//
//  This file is part of GPSTk, the GPS Toolkit.
//
//  The GPSTk is free software; you can redistribute it and/or modify
//  it under the terms of the GNU Lesser General Public License as published
//  by the Free Software Foundation; either version 2.1 of the License, or
//  any later version.
//
//  The GPSTk is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public
//  License along with GPSTk; if not, write to the Free Software Foundation,
//  Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//  
//  Copyright 2004, The University of Texas at Austin
//
//============================================================================


#ifndef VPLOT_HELPER_H
#define VPLOT_HELPER_H

#include "VGImage.hpp"
#include "SVGImage.hpp"
#include "PSImage.hpp"
#include "EPSImage.hpp"

namespace vplot
{
  /** \defgroup BasicVectorGraphics Basic Vector Graphics*/ 
  //@{

  /**
   * Helper class contains static helper methods for common 
   * code related to this library.
   */
  class Helper
  {
    /**
     * Get a VGImage pointer decided by the filename extension.  
     * - filename.svg == SVImage*
     * - filename.ps  == PSImage*
     * - filename.eps == EPSImage*
     * @note This does not necessarily cover all constructors of all of
     * these classes but in general will cover the most cases.
     * @param fname The file name to create an image for
     * @param width Width of the canvas in points
     * @param height Height of the canvas in points
     * @param iloc Location on the page of the overall origin
     */
    public static VGImage* create(std::string fname,
        double width=US_LETTER_WIDTH_PTS,
        double height=US_LETTER_HEIGHT_PTS,
        ORIGIN_LOCATION iloc=LOWER_LEFT) throw (VPlotException)
    {
      using namespace std;
      size_t i = fname.find_last_of('.');
      if ((string::npos != i) && (i != fname.length()-1))
      {
        string ext = fname.substr(i+1);
        if( ext == "ps" )
          return new PSImage(fname.c_str(),width,height,iloc);
        else if( ext == "eps" )
          return new EPSImage(fname.c_str(),0,0,width,height,iloc);
        else if( ext == "svg" )
          return new SVGImage(fname.c_str(),width,height,iloc);
      }
      throw VPlotException("Non-supported file name...");
    }

  }; // class Helper

  //@} group BasicVectorGraphics

} // namespace vplo

#endif //VPLOT_HELPER_H
