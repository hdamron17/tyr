@intfmt = private constant [4 x i8] c"%d\0A\00"

declare i32 @printf(i8*, ...) #1

define void @_print_i(i32 %v) #1 {
  call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @intfmt, i32 0, i32 0), i32 %v)
  ret void
}
