
const render = require('./lib/render');
const logger = require('koa-logger');
const router = require('koa-router')();
const koaBody = require('koa-body');
const fs = require('mz/fs');

const Koa = require('koa');
const app = module.exports = new Koa();

// middleware

app.use(logger());

app.use(render);

app.use(koaBody());

// route definitions

router.get('/', list)
      .get('/logs/:id', show);

app.use(router.routes());

/**
 * log listing.
 */

async function list(ctx) {
  const logfilesAll = await fs.readdir("logs");
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
        prefix: prefix
    }
  });
  await ctx.render('list', { logs: logs });
}

/**
 * Show creation form.
 */

async function add(ctx) {
  await ctx.render('new');
}

/**
 * Show log :id.
 */

async function show(ctx) {
  const id = ctx.params.id;
  const body = await fs.readFile("logs/" + id, 'utf8');
  const log = {
    title: id,
    body: body
  };
  if (!log) ctx.throw(404, 'invalid log id');
  await ctx.render('show', { log: log });
}

// listen

if (!module.parent) app.listen(3000);
