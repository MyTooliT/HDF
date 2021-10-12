# -- Variables -----------------------------------------------------------------

ifeq ($(OS),Windows_NT)
	clean_command=powershell rm Data/*.csv Data/*.hdf5
else
	clean_command=rm -f Data/*.csv Data/*.hdf5
endif

# -- Rules ---------------------------------------------------------------------

all:
	python Source/convert.py

clean:
	$(clean_command)
