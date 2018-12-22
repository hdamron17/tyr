@intfmt = private constant [4 x i8] c"%d\0A\00"

declare i32 @printf(i8*, ...) #1

define i32 @main() #0 {
  %1 = alloca i32, align 4
  store i32 42, i32* %1
  %r1 = load i32, i32* %1
  call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @intfmt, i32 0, i32 0), i32 %r1)
  ret i32 0
}
