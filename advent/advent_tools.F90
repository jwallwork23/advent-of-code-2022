module advent_tools
  implicit none

  contains

    integer function bin2dec(b, l)
      ! """
      ! Convert an integer from binary form to decimal form.
      !
      ! :arg b: the integer, written in binary form as a character string
      ! :arg l: the length of the character string
      ! :return: the integer as a decimal integer
      ! """
      implicit none
      character(len=*), intent(in) :: b
      integer, intent(in) :: l
      integer :: i

      bin2dec = 0
      do i = l,1,-1
        if (b(i:i) == "1") then
          bin2dec = bin2dec + 2 ** (l - i)
        end if
      end do
    end function bin2dec

    integer function triangle(i)
      ! """
      ! Compute the triangle of an integer.
      !
      ! :arg i: the integer
      ! :return: the corresponding triangular number
      ! """
      implicit none
      integer, intent(in) :: i
      integer :: j

      triangle = 0
      do j = 1,i
        triangle = triangle + j
      end do
    end function triangle

    integer function factorial(i)
      ! """
      ! Compute the factorial of an integer.
      !
      ! :arg i: the integer
      ! :return: the corresponding factorial
      ! """
      implicit none
      integer, intent(in) :: i
      integer :: j

      factorial = 1
      do j = 1,i
        factorial = factorial * j
      end do
    end function factorial

    integer(kind=8) function factorial8(i)
      ! """
      ! Compute the factorial of an integer as an 8-byte integer.
      !
      ! :arg i: the integer
      ! :return: the corresponding factorial
      ! """
      implicit none
      integer, intent(in) :: i
      integer :: j

      factorial8 = 1
      do j = 1,i
        factorial8 = factorial8 * j
      end do
    end function factorial8

    subroutine bubble_sort(array)
      ! """
      ! Apply the bubble sort algorithm to an array of integers.
      !
      ! :arg array: the array of integers, which gets modified in-place
      ! """
      implicit none
      integer, dimension(:), intent(in out) :: array
      integer :: i, j, tmp

      do i = size(array)-1,1,-1
        do j = 1,i
          if (array(j+1) < array(j)) then
            tmp = array(j+1)
            array(j+1) = array(j)
            array(j) = tmp
          end if
        end do
      end do
    end subroutine bubble_sort

    subroutine bubble_sort8(array)
      ! """
      ! Apply the bubble sort algorithm to an array of 8-byte integers.
      !
      ! :arg array: the array of integers, which gets modified in-place
      ! """
      implicit none
      integer(kind=8), dimension(:), intent(in out) :: array
      integer :: i, j, tmp

      do i = size(array)-1,1,-1
        do j = 1,i
          if (array(j+1) < array(j)) then
            tmp = array(j+1)
            array(j+1) = array(j)
            array(j) = tmp
          end if
        end do
      end do
    end subroutine bubble_sort8

end module advent_tools
