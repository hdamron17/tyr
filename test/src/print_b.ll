@true = private constant [5 x i8] c"true\00"
@false = private constant [6 x i8] c"false\00"

declare i32 @puts(i8*) #1

define void @_print_b(i1 %b) #1 {
  %1 = add i32 0, 0
  br i1 %b, label %t, label %f
t:
  call i32 (i8*) @puts(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @true, i32 0, i32 0))
  br label %end
f:
  call i32 (i8*) @puts(i8* getelementptr inbounds ([6 x i8], [6 x i8]* @false, i32 0, i32 0))
  br label %end
end:
  %4 = add i32 %1, 9
  ret void
}

define i32 @main() #0 {
  call void (i1) @_print_b(i1 1)
  call void (i1) @_print_b(i1 0)
  ret i32 0
}
