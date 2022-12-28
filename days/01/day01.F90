program day01
  implicit none

#if TEST
  character(len=8), parameter :: fname = "test.txt"
#else
  character(len=9), parameter :: fname = "input.txt"
#endif
  integer, parameter :: npad = 100

  character(len=80) :: line
  integer :: nelf = 1
  integer :: tmp
  integer :: elf(npad)
  integer :: m1 = -1
  integer :: m2 = -2
  integer :: m3 = -3

  open(unit=99, file=fname)
  do
    read(unit=99, end=100, fmt="(a)") line
    if (index(line, " ") == 1) then
      call chk(elf(nelf))
      nelf = nelf + 1
    else
      read(unit=line, fmt="(i)") tmp
      elf(nelf) = elf(nelf) + tmp
    end if
  end do
  100 close(unit=99)
  call chk(elf(nelf))
  print *, "Part 1: ", m1
  print *, "Part 2: ", m1 + m2 + m3

  contains

    subroutine chk(val)
      ! """
      ! Compare a value against the current maxima.
      !
      ! :arg val: the value to compare
      ! """
      implicit none
      integer, intent(in) :: val

      if (val >= m1) then
        m3 = m2
        m2 = m1
        m1 = val
      else if (val >= m2) then
        m3 = m2
        m2 = val
      else if (val >= m3) then
        m3 = max(val, m3)
        m3 = val
      end if
    end subroutine chk

end program day01
