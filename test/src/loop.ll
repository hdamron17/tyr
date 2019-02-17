define i32 @main() #0 {
  %1 = alloca i32
  store i32 0, i32* %1
  %2 = alloca i32
  store i32 0, i32* %2
  br label %for1
for1:
  %3 = load i32, i32* %1
  %4 = icmp slt i32 %3, 8
  br i1 %4, label %body1, label %afterfor1
body1:
  %5 = load i32, i32* %2
  %6 = add i32 %5, 3
  store i32 %6, i32* %2
  br label %endfor1
endfor1:
  %7 = load i32, i32* %1
  %8 = add i32 %7, 1
  store i32 %8, i32* %1
  br label %for1
afterfor1:
  %9 = load i32, i32* %2
  ret i32 %9
}
