const gulp = require("gulp");
const uglify = require('gulp-uglify');
const changed = require('gulp-changed');
const cleanCSS = require("gulp-clean-css");
const rev = require('gulp-rev');
const revFormat = require('gulp-rev-format');
const sourcemaps = require('gulp-sourcemaps');

const CSS_DESTINATION = 'compiled_staticfiles/css';
const JS_DESTINATION = 'compiled_staticfiles/js';

function minifyCSS() {
    return (
        gulp.src("./static/css/*.css", '!./static/css/*.min.css')
            .pipe(changed(CSS_DESTINATION))
            .pipe(cleanCSS())
            .pipe(rev())
            .pipe(revFormat({
                prefix: '.',
                suffix: '.min'
            }))
            .pipe(rev.manifest('manifest.json'))
            .pipe(gulp.dest(CSS_DESTINATION))
    )
}

function minifyJS() {
    return (
        gulp.src(['./static/js/*.js', '!./static/js/*.min.js'])
            .pipe(sourcemaps.init({loadMaps: true, largeFile: true}))
            .pipe(changed(JS_DESTINATION))
            .pipe(uglify())
            .pipe(rev())
            .pipe(revFormat({
                prefix: '.',
                suffix: '.min'
            }))
            .pipe(sourcemaps.write())
            .pipe(rev.manifest('manifest.json'))
            .pipe(gulp.dest(JS_DESTINATION))
    )
}

gulp.task("minify-css", minifyCSS);
gulp.task("minify-js", minifyJS);

gulp.task('build', gulp.series('minify-css', 'minify-js'));
