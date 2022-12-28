all: run

CODE	= ${HOME}/src/advent_of_code/2022/advent
FC	= ifort
FFLAGS	=
LDFLAGS	= $(CODE)/advent_tools.F90
EXE	= day01

run: clean
	@$(FC) $(FFLAGS) $(LDFLAGS) $(EXE).F90 -o $(EXE)
	@./$(EXE)

test: clean
	@$(FC) $(FFLAGS) -DTEST $(LDFLAGS) $(EXE).F90 -o $(EXE)
	@./$(EXE)

clean:
	@rm -f $(EXE) *.mod *.o
