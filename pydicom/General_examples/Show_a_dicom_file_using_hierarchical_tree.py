from __future__ import print_function

from pydicom import compat

if compat.in_py2:
    import Tix as tkinter_tix
else:
    import tkinter.tix as tkinter_tix

print(__doc__)

usage = "python General_examples/Show_a_dicom_file_using_hierarchical_tree.py rtplan2.dcm"

def Runtree(w, filename):
    top = tkinter_tix.Frame(w, relief=tkinter_tix.RAISED, bd=1)
    tree = tkinter_tix.Tree(top, options="hlist.columns 2")
    tree.pack(expand=1, fill=tkinter_tix.BOTH, padx=10, pady=10, side=tkinter_tix.LEFT)
    tree.hlist.configure(bg='white', font='Courier 10', indent=30)
    tree.hlist.configure(selectbackground='light yellow', gap=150)

    box = tkinter_tix.ButtonBox(w, orientation=tkinter_tix.HORIZONTAL)
    box.add('ok', text='OK', underline=0, command=w.destroy, width=6)
    box.add('exit', text='Exit', underline=0, command=w.destroy, width=6)
    box.pack(side=tkinter_tix.BOTTOM, fill=tkinter_tix.X)
    top.pack(side=tkinter_tix.TOP, fill=tkinter_tix.BOTH, expand=1)

    tree.bind_all('<MouseWheel>', lambda event: tree.hlist.
                  yview_scroll(int(-1 * event.delta / 120.), "units"))
    tree.bind_all('<Button-4>', lambda event: tree.hlist.
                  yview_scroll(int(-1), "units"))
    tree.bind_all('<Button-5>', lambda event: tree.hlist.
                  yview_scroll(int(+1), "units"))
    show_file(filename, tree)


def show_file(filename, tree):
    tree.hlist.add("root", text=filename)
    ds = pydicom.dcmread(sys.argv[1])
    ds.decode()
    recurse_tree(tree, ds, "root", False)
    tree.autosetmode()


def recurse_tree(tree, dataset, parent, hide=False):
    for data_element in dataset:
        node_id = parent + '.' + hex(id(data_element))
        if isinstance(data_element.value, compat.text_type):
            tree.hlist.add(node_id, text=compat.text_type(data_element))
        else:
            tree.hlist.add(node_id, text=str(data_element))
        if hide:
            tree.hlist.hide_entry(node_id)
        if data_element.VR == "SQ":
            for i, dataset in enumerate(data_element.value):
                item_id = node_id + "." + str(i + 1)
                sq_item_description = data_element.name.replace(" Sequence", "")
                item_text = "{} {}".format(sq_item_description, i + 1)
                tree.hlist.add(item_id, text=item_text)
                tree.hlist.hide_entry(item_id)
                recurse_tree(tree, dataset, item_id, hide=True)

if __name__ == '__main__':
    import sys
    import pydicom

    if len(sys.argv) != 2:
        print("Please supply a dicom file name:\n")
        print(usage)
        sys.exit(-1)
    root = tkinter_tix.Tk()
    root.geometry('{}x{}+{}+{}'.format(1200, 900, 0, 0))
    root.title("DICOM tree viewer - " + sys.argv[1])

    Runtree(root, sys.argv[1])
    root.mainloop()
