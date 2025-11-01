export default {
  async fetch(req: Request): Promise<Response> {
    const url = new URL(req.url);
    if (url.pathname==='/feed')  return new Response(JSON.stringify([{t:'Bem-vindo'}]),{headers:{'content-type':'application/json'}});
    if (url.pathname==='/ranking')return new Response(JSON.stringify([{user:'alpha',score:98}]),{headers:{'content-type':'application/json'}});
    return new Response('OK');
  }
}