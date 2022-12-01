all: run

CODE	= ${HOME}/src/advent_of_code/2022/advent
FC		= nvfortran
FFLAGS	=
LDFLAGS	= $(CODE)/advent_tools.F90
EXE		= dayX

run: clean
	@$(FC) $(FFLAGS) $(LDFLAGS) $(EXE).F90 -o $(EXE)
	@./$(EXE)

test: clean
	@$(FC) $(FFLAGS) -DTEST $(LDFLAGS) $(EXE).F90 -o $(EXE)
	@./$(EXE)

clean:
	@rm -f $(EXE) *.mod *.o
