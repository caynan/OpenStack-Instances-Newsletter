var gulp = require('gulp'),
    inline = require('gulp-inline-css');

gulp.task('inline', function(){
  gulp.src('email_template/src/*.html')
  .pipe(inline())
  .pipe(gulp.dest('email_template'));
});

gulp.task('watch', function(){
  gulp.watch('email_template/src/*.html', ['inline']);
});


gulp.task('default', ['inline', 'watch']);
