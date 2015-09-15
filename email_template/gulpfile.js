var gulp = require('gulp'),
    inline = require('gulp-inline-css'),
    imagemin = require('gulp-imagemin');

// Inline Task
// Inline all css
gulp.task('inline', function(){
  gulp.src('src/*.html')
  .pipe(inline())
  .pipe(gulp.dest('build'));
});

// Image Task
// Compress all images, to reduce email size
gulp.task('image', function(){
  gulp.src('img/**')
  .pipe(imagemin())
  .pipe(gulp.dest('img'));
});

// Watch Task
// Keep gulp running and watching for changes
gulp.task('watch', function(){
  gulp.watch('src/*.html', ['inline', 'image']);
});

// Default Task
// What is called when you call gulp without args
gulp.task('default', ['inline', 'image', 'watch']);
