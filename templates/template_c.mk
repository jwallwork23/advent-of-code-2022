all: run

CODE	= ${HOME}/src/advent_of_code/2022/advent
CC		= nvcc
CFLAGS	=
LDFLAGS	= -I$(CODE) $(CODE)/advent_tools.c
EXE		= dayX

run: clean
	@$(CC) $(CFLAGS) $(LDFLAGS) $(EXE).c -o $(EXE)
	@./$(EXE)

test: clean
	@$(CC) $(CFLAGS) -DTEST $(LDFLAGS) $(EXE).c -o $(EXE)
	@./$(EXE)

clean:
	@rm -f $(EXE) *.o
