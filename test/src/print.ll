@intfmt = private constant [4 x i8] c"%s\0A\00"
@str = private constant [12 x i8] c"Hello world\00"

declare i32 @printf(i8*, ...) #1
declare i32 @puts(i8*) #1

define i32 @main() #0 {
  call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @intfmt, i32 0, i32 0),
                              i8* getelementptr inbounds ([12 x i8], [12 x i8]* @str, i32 0, i32 0))
  call i32 (i8*) @puts(i8* getelementptr inbounds ([12 x i8], [12 x i8]* @str, i32 0, i32 0))
  ret i32 0
}
