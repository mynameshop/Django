var gulp = require("gulp");
var typescript = require("gulp-typescript");
var merge2 = require("merge2");
var concat = require("gulp-concat");
var cleants = require('gulp-clean-ts-extends');
var runSequence = require('run-sequence');
var replace = require("gulp-replace");
var expect = require('gulp-expect-file');
var clean = require('gulp-clean');
var config = require("./config.json");
var rename = require("gulp-rename");
var uglify = require('gulp-uglify');

var extendsSearchRegex = /var\s__extends[\s\S]+?\};/g;
var decorateSearchRegex = /var\s__decorate[\s\S]+?\};/g;

gulp.task('typescript-compile', function () {
    return gulp.src(config.core.typescript).
        pipe(typescript({
            noExternalResolve: true,
            removeComments: true,
            target: 'ES5',
            typescript: require('typescript'),
            experimentalDecorators: true
        }))
        .pipe(gulp.dest(config.build.srcOutputDirectory));
});

function generateFinalJs(src, name) {
    return gulp.src(src)
    	.pipe(expect.real({ errorOnFailure: true }, src))
        .pipe(concat(name))
        .pipe(cleants())
        .pipe(replace(extendsSearchRegex, ""))
        .pipe(replace(decorateSearchRegex, ""))
        .pipe(gulp.dest(config.build.outputDirectory))
}

gulp.task("build", function () {
    return merge2(
        gulp.src(config.core.files).
            pipe(expect.real({ errorOnFailure: true }, config.core.files)),
        gulp.src(config.editor.files).
            pipe(expect.real({ errorOnFailure: true }, config.editor.files)),
        generateFinalJs(config.core.files, config.build.appFilename),
        generateFinalJs(config.editor.files, config.build.editorFilename),
        generateFinalJs(config.pbrEditor.files, config.build.pbrEditorFilename)
    );
});

gulp.task("compile_api", function () {
	return gulp.src(config.api.typescript)
	    .pipe(typescript({
	        noExternalResolve: true,
	        removeComments: true,
	        target: 'ES5',
	        typescript: require('typescript'),
	        experimentalDecorators: true
	    }))
	    .pipe(uglify())
	    .pipe(gulp.dest(config.build.srcOutputDirectory))
});

gulp.task("build_api", function () {
	return merge2(
        gulp.src(config.api.files).pipe(expect.real({ errorOnFailure: true }, config.api.files)),
        generateFinalJs(config.api.files, config.build.apiFilename)
	)
});

gulp.task('compress_api', function () {
	return gulp.src(['static/js/lib/babylon-2.5.min.js', config.build.outputDirectory + config.build.apiFilename])
		.pipe(concat(config.build.apiFilename))
	    .pipe(gulp.dest(config.build.outputDirectory))
})

gulp.task("clean", function () {
	return gulp.src(config.build.srcOutputDirectory, {read: false})
    .pipe(clean());
});

gulp.task('default', function (cb) {
    runSequence("typescript-compile", "build", "compile_api", "build_api", "compress_api", "clean", cb);
});