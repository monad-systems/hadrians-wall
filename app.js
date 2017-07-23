const serve = require('koa-static');
const render = require('./lib/render');
const logger = require('koa-logger');
const router = require('koa-router')();
const koaBody = require('koa-body');
const querystring = require('querystring');
const fs = require('mz/fs');
const Koa = require('koa');
const app = module.exports = new Koa();

// middleware

app.use(logger());

app.use(render);

app.use(koaBody());

// route definitions

router.get('/', list);

app.use(serve('static'));

app.use(router.routes());

/**
 * log listing.
 */

async function list(ctx) {
  const logfilesAll = await fs.readdir("static/logs");
  const logfilesNames = logfilesAll.filter(function (f) {
    return f.search("err") == -1;
  });
  const logs = logfilesNames.map(function (f) {
    const prefix = f.slice(0, -8);
    const segments = prefix.split("%");
    return {
        time: new Date(segments[0]),
        type: segments[1],
        length: parseFloat(segments[2]) / 60.0,
        status: segments[3],
        prefix: querystring.escape(prefix)
    }
  });

  await ctx.render('index', { logs: logs });
}

// listen

if (!module.parent) app.listen(3000);
