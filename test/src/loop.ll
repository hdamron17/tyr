define i32 @main() #0 {
  %1 = alloca i3
  store i32 42, i32* %1
lp:
  %2 = add i32 4, 5
  %3 = load i32, i32* %1
  br label %lp
  ret i32 %3
}
