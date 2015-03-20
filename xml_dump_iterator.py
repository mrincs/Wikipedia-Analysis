# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 18:05:08 2015

@author: mrinmoymaity: Written in Python-3.4
"""

from mw.xml_dump import Iterator
from mw.xml_dump import Page
from mw.xml_dump import Revision
from mw.lib import reverts





def find_user(edit_list, rev_id):
    for i in range(len(edit_list)):
        if edit_list[i][0] == rev_id:
            key = edit_list[i][1]
    if key != None:
        return key
    else:
        return -1

# Construct dump file iterator

def parse_revisions():
    dump_iter = Iterator.from_file(open(xml_stub_history,encoding='latin-1'))
    #print("------------Site Metadata----------------", file=output_file)
    #print("\nSiteName: ",dump_iter.site_name,"\nBase: ",dump_iter.base,"\nGenerator:        ",dump_iter.generator,"\nCase: ",dump_iter.case, file=output_file)
      
      #page_iter_idx = 0 # Number of pages
      #cumulative_rev_iter_idx = 0 # Total number of revisions of all pages
      ## Iterate through pages
      #for page_iter in dump_iter:
      #    page_iter_idx = page_iter_idx+1
      #    rev_iter_idx = 0
      #    # Iterate through a page's revisions
      #    for revision_iter in page_iter:
      #        rev_iter_idx = rev_iter_idx+1
      #        cumulative_rev_iter_idx = cumulative_rev_iter_idx+1
      #        #print(revision_iter.id)
      #        
      #print(page_iter_idx, cumulative_rev_iter_idx)

    page_iter_idx = 0 # Number of pages
    for page_iter in dump_iter:
        if page_iter_idx < 1000:
            page_iter_idx = page_iter_idx+1
            page = Page(page_iter.id, page_iter.title, page_iter.namespace,  page_iter.redirect, page_iter.restrictions, page_iter.__iter__()) 
            #print("\n",page_iter_idx,". PageID: ",page.id, file=output_file)
            print("#", file=output_file)
            rev_iter_idx = 0
            detector = reverts.Detector()
            edit_list = []
            for rev_iter in page:
                rev_iter_idx = rev_iter_idx+1
#                revision = Revision(rev_iter.id, rev_iter.timestamp)
                edit_list.append([rev_iter.id, rev_iter.contributor.id])
                #print(edit_list, file=output_file)
                #print("\n\t",rev_iter_idx,".",rev_iter,"\n", file=output_file)
                revert_info = detector.process(rev_iter.sha1, rev_iter.id)
                if revert_info != None:
                    reverter = find_user(edit_list, revert_info.reverting) 
                    revertedTo = find_user(edit_list, revert_info.reverted_to)
                    for i in range(len(revert_info.reverteds)):
                        reverted = find_user(edit_list, revert_info.reverteds[i])
                        print(reverter,",",revertedTo,",",reverted, file=output_file)



xml_stub_history = "C:\WikiProject\simplewiki-20141222-stub-meta-history.xml"
xml_stub_current = "C:\WikiProject\simplewiktionary-20150123-stub-meta-current.xml"
output_file = open('revision_1000.log', mode='w', encoding='utf-8')
parse_revisions()
output_file.close()
#a = [[21,34],[31,22],[1,4],[4,6],[34,25],[4,6]]
#print(find_user(a,1))                    