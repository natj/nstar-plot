"""
-------------------------------------------------------------------

Copyright (C) 2015-2016, Andrew W. Steiner

This neutron star plot is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3 of
the License, or (at your option) any later version.

This neutron star plot is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this neutron star plot. If not, see
<http://www.gnu.org/licenses/>.

-------------------------------------------------------------------

"""

import h5py
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plot

list_of_dsets=[]

# H5py read function from O2scl
def hdf5_is_object_type(name,obj):
    if isinstance(obj,h5py.Group):
        if 'o2scl_type' in obj.keys():
            o2scl_type_dset=obj['o2scl_type']
            if o2scl_type_dset.__getitem__(0) == search_type:
                list_of_dsets.append(name)
                
""" -------------------------------------------------------------------
Class definition
"""
class eos_mvsr_plot:
    fig=0
    ax1=0
    ax2=0

    # Default plot function from O2scl
    def default_plot(self,lmar=0.14,bmar=0.12,rmar=0.04,tmar=0.04):
        plot.rc('text',usetex=True)
        plot.rc('font',family='serif')
        plot.rcParams['lines.linewidth']=0.5
        self.fig,(self.ax1,self.ax2) = plot.subplots(1,2,figsize=(10.0,6.0))
        self.fig.subplots_adjust(wspace=0.2,left=0.08,right=0.98,
                                 bottom=0.12,top=0.97)
        self.ax1.minorticks_on()
        self.ax1.tick_params('both',length=10,width=1,which='major')
        self.ax1.tick_params('both',length=5,width=1,which='minor')
        self.ax2.minorticks_on()
        self.ax2.tick_params('both',length=10,width=1,which='major')
        self.ax2.tick_params('both',length=5,width=1,which='minor')
        self.fig.set_facecolor('white')
        plot.grid(False)

    # H5py read function from O2scl
    def h5read_type_named(self,fname,loc_type,name):
        del list_of_dsets[:]
        global search_type
        search_type=loc_type
        file=h5py.File(fname,'r')
        file.visititems(hdf5_is_object_type)
        if name in list_of_dsets:
            return file[name]
            str=('No object of type '+loc_type+' named '+name+
                 ' in file '+fname+'.')
            raise RuntimeError(str)
            return

    # Main run()
    def run(self):
        self.default_plot()
        dset=self.h5read_type_named('eos.o2','table','full_eos')
        # Convert to MeV/fm^3
        ed2=[dset['data/ed'][i]*197.33 for i in 
             range(0,len(dset['data/ed']))]
        pr2=[dset['data/pr'][i]*197.33 for i in 
             range(0,len(dset['data/pr']))]
        self.ax1.set_ylim([1.0e-1,1.0e3])
        self.ax1.set_xlim([0,1600])
        self.ax1.semilogy(ed2,pr2)
        self.ax1.text(0.5,-0.08,
                      r'$\varepsilon~(\mathrm{MeV}/\mathrm{fm}^3)$',
                      fontsize=24,va='center',ha='center',
                      transform=self.ax1.transAxes)
        self.ax1.text(-0.1,0.5,
                      r'$P~(\mathrm{MeV}/\mathrm{fm}^3)$',
                      fontsize=24,va='center',ha='center',
                      transform=self.ax1.transAxes,rotation=90)
        dset=self.h5read_type_named('mvsr.o2','table','mvsr')
        self.ax2.set_ylim([0.0,2.1])
        self.ax2.set_xlim([8,24])
        self.ax2.plot(dset['data/r'],dset['data/gm'])
        self.ax2.text(0.5,-0.08,'$R~(\mathrm{km})$',
                      fontsize=24,va='center',ha='center',
                      transform=self.ax2.transAxes)
        self.ax2.text(-0.1,0.6,'$M~(\mathrm{M}_{\odot})$',
                      fontsize=24,va='center',ha='center',
                      transform=self.ax2.transAxes,rotation=90)
        #
        self.fig.text(0.41,0.37,(r'$\leftarrow \stackrel{\frac{dP}{dr}='+
                                 r'-\frac{G m \varepsilon}'+
                                 r'{r^2}\left(1+\frac{P}{\varepsilon}\right)'+
                                 r'\left(1+\frac{4 \pi P r^3}{m}\right)'+
                                 r'\left(1-\frac{2 G m}{r}\right)^{-1}}'+
                                 r'{\scriptstyle{1-1~~'+
                                 r'\mathrm{correspondence}}}'+
                                 r'\rightarrow$'),
                      fontsize=28,va='center',ha='center',
                      transform=self.ax1.transAxes,zorder=10,
                      bbox=dict(facecolor=(0.75,0.75,1.0),lw=0))
        plot.savefig('eos_mvsr.png')
        plot.savefig('eos_mvsr.eps')
        plot.show()

""" -------------------------------------------------------------------
Create the plot
"""

em=eos_mvsr_plot()
em.run()
