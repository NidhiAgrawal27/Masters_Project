import graph_tool as gt
import graph_tool.dynamics as gtd
import graph_tool.inference as gti
import graph_tool.topology as gtt
from graph_tool import draw
import numpy as np
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
from utilities.visualization import plot_modularity_graph
from multiprocessing import Process, Pool, Manager, Value
import functools
from threading import Thread
from threading import Lock

class Modularity:
    def __init__(self):      
        self.no_entities = Manager().Value('i',0)
        self.component_number = Manager().Value('i',0)

    def label_prop(self,gin, max_iter = 100, each_update = None):
        try:  
            no_nodes = gin.num_vertices()
            if each_update is None:
                each_update = gin.num_edges()

            lp = gtd.MajorityVoterState(gin, q=no_nodes+1 )
            for _ in range(no_nodes):
                lp.get_state().fa[_] = _+1

            converged = False
            i_iter = 0    

            while not converged and i_iter < max_iter:
                ret = lp.iterate_async(each_update)
                converged = (ret == 0)
                i_iter += 1

            return lp.get_state()
        
        except:
            raise Exception("Error calculating Label Propagation!")

    def multiprocess_component_calc(self,i_comp,components,heuristic,g):
        prop_list = {}
        lock = Lock()

        lock.acquire()
        self.component_number.value += 1
        lock.release()

        try:
            # boolean vector components map
            vec_comp = components == i_comp

            # no. of vertices belonging to the particular component- size of the component        
            comp_size =  int(np.sum(vec_comp))

            if heuristic == "h0_h1":
                comp_edges = gt.GraphView(g, vfilt = vec_comp).num_edges()
                return comp_size, comp_edges, None, None, None

            # giving the unique label for small communities
            if (np.sum(vec_comp) < 6 or np.sum(vec_comp)>1000000) and heuristic=="h0":
                lock.acquire()
                for v in np.where(vec_comp)[0]:
                    v_index = int(v)
                    prop_list[v_index] = self.no_entities.value
                self.no_entities.value += 1
                lock.release()
                comp_edges = gt.GraphView(g, vfilt = vec_comp).num_edges()
                comp_comm = 1
                comp_mod = 0

            else:
                gv= gt.GraphView(g, vfilt = vec_comp)    
                redv = defaultdict(lambda : self.no_entities.value+len(redv))
                communities = self.label_prop(gv, 20)

                lock.acquire()
                for v in gv.vertices():
                    v_index = int(v)
                    prop_list[v_index] = redv[communities[v]]
                self.no_entities.value += len(redv)
                lock.release()
                
                #store number of edges dictionary with component size
                comp_edges = gv.num_edges()

                #store number of communities dictionary with component size
                comp_comm = len(set(communities.fa))

                #calculate modularity for only components having more than one community
                if len(set(communities.fa))>1:
                    comp_mod = gti.modularity(gv,communities)
                else: comp_mod = 0

            #returns empty communities, modularity and entities for h0_h1 heuristic
            return comp_size, comp_edges, comp_comm, comp_mod, prop_list
        
        except:
            raise Exception("Error getting results in component {}!".format(self.component_number.value))


    def compute_modularity(self, g, components, heuristic):
        
        entities = g.new_vertex_property("int")
        component_labels = np.unique( components.a )

        print('\nModularity Progress Bar:')
        pool = Pool(processes=16)
        try:
            sz_comp_size, sz_comp_edges, sz_comp_comm, sz_comp_mod, prop_dict_list = zip(*pool.map(functools.partial(self.multiprocess_component_calc,components=components.a,heuristic=heuristic,g=g),tqdm(component_labels)))
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            pool.terminate()
        finally:
            pool.terminate()
        print("Modularity computed. Joining different process results")

        if heuristic=="h0":
            prop_dict = {key:value for subdict in prop_dict_list for key,value in subdict.items()}
            
            for key,value in prop_dict.items():
                entities[g.vertex(key)] = value

            #returns empty communities, modularity and entities for h0_h1 heuristic
            return sz_comp_size, sz_comp_edges, sz_comp_comm, sz_comp_mod, entities
        else:
            return sz_comp_size, sz_comp_edges, None, None, None