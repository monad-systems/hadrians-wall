
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
      .get('/log/:id', show);

app.use(router.routes());

/**
 * log listing.
 */

async function list(ctx) {
  const logs = await fs.readdir("logs");
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
