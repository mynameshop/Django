// npm install gulp gulp-chug gulp-clean gulp-typescript merge2 gulp-concat gulp-clean-ts-extends run-sequence gulp-replace gulp-expect-file --save-dev
var gulp = require( 'gulp' );
var chug = require( 'gulp-chug' );
var gutil = require('gulp-util');
var runSequence = require('run-sequence');
var nunjucks = require('gulp-nunjucks');
var path = require('path');
var concat = require('gulp-concat');

gulp.task( 'default', function (cb) {
    gulp.src( './apps/**/gulpfile.js' ).pipe(
    	chug({
    		tasks: [ 'default' ]
    	})
    );
    runSequence("build_templates", cb);
});

gulp.task('build_templates', function (cb) {
	gulp.src('apps/**/jinja2/**/common/**.html')
	.pipe(nunjucks.precompile({name: function(file){
		return path.basename(file.path)
	}}))
	.pipe(concat('templates.js'))
    .pipe(gulp.dest('static/js'))
});

gulp.task('watch', function() {
	gulp.watch('apps/**/jinja2/**/common/**.html', ['buld_templates']);
});
