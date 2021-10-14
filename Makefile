# -- Variables -----------------------------------------------------------------

ifeq ($(OS),Windows_NT)
	rm := powershell rm
	clean_command := $(rm) Data/*.csv; $(rm) Data/*.hdf5
else
	clean_command := rm -f Data/*.csv Data/*.hdf5
endif

# -- Rules ---------------------------------------------------------------------

all:
	python Source/convert.py

clean:
	$(clean_command)
