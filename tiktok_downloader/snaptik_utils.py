from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['_0xe48c', 'decoder', '_0xc38e'])
@Js
def PyJsHoisted__0xe48c_(d, e, f, this, arguments, var=var):
    var = Scope({'d':d, 'e':e, 'f':f, 'this':this, 'arguments':arguments}, var)
    var.registers(['f', 'k', 'd', 'h', 'i', 'e', 'j', 'g'])
    var.put('g', var.get('_0xc38e').get('2').callprop(var.get('_0xc38e').get('1'), var.get('_0xc38e').get('0')))
    var.put('h', var.get('g').callprop(var.get('_0xc38e').get('3'), Js(0.0), var.get('e')))
    var.put('i', var.get('g').callprop(var.get('_0xc38e').get('3'), Js(0.0), var.get('f')))
    @Js
    def PyJs_anonymous_0_(a, b, c, this, arguments, var=var):
        var = Scope({'a':a, 'b':b, 'c':c, 'this':this, 'arguments':arguments}, var)
        var.registers(['b', 'c', 'a'])
        if PyJsStrictNeq(var.get('h').callprop(var.get('_0xc38e').get('4'), var.get('b')),(-Js(1.0))):
            return var.put('a', (var.get('h').callprop(var.get('_0xc38e').get('4'), var.get('b'))*var.get('Math').callprop(var.get('_0xc38e').get('8'), var.get('e'), var.get('c'))), '+')
    PyJs_anonymous_0_._set_name('anonymous')
    var.put('j', var.get('d').callprop(var.get('_0xc38e').get('1'), var.get('_0xc38e').get('0')).callprop(var.get('_0xc38e').get('10')).callprop(var.get('_0xc38e').get('9'), PyJs_anonymous_0_, Js(0.0)))
    var.put('k', var.get('_0xc38e').get('0'))
    while (var.get('j')>Js(0.0)):
        var.put('k', (var.get('i').get((var.get('j')%var.get('f')))+var.get('k')))
        var.put('j', ((var.get('j')-(var.get('j')%var.get('f')))/var.get('f')))
    return (var.get('k') or var.get('_0xc38e').get('11'))
PyJsHoisted__0xe48c_.func_name = '_0xe48c'
var.put('_0xe48c', PyJsHoisted__0xe48c_)
@Js
def PyJsHoisted_decoder_(h, u, n, t, e, r, this, arguments, var=var):
    var = Scope({'h':h, 'u':u, 'n':n, 't':t, 'e':e, 'r':r, 'this':this, 'arguments':arguments}, var)
    var.registers(['len', 'r', 's', 'h', 'u', 'i', 'n', 'e', 't', 'j'])
    var.put('r', Js(''))
    #for JS loop
    var.put('i', Js(0.0))
    var.put('len', var.get('h').get('length'))
    while (var.get('i')<var.get('len')):
        try:
            var.put('s', Js(''))
            while PyJsStrictNeq(var.get('h').get(var.get('i')),var.get('n').get(var.get('e'))):
                var.put('s', var.get('h').get(var.get('i')), '+')
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            #for JS loop
            var.put('j', Js(0.0))
            while (var.get('j')<var.get('n').get('length')):
                try:
                    var.put('s', var.get('s').callprop('replace', var.get('RegExp').create(var.get('n').get(var.get('j')), Js('g')), var.get('j')))
                finally:
                        (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
            var.put('r', var.get('String').callprop('fromCharCode', (var.get('_0xe48c')(var.get('s'), var.get('e'), Js(10.0))-var.get('t'))), '+')
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    return var.get('decodeURIComponent')(var.get('escape')(var.get('r')))
PyJsHoisted_decoder_.func_name = 'decoder'
var.put('decoder', PyJsHoisted_decoder_)
var.put('_0xc38e', Js([Js(''), Js('split'), Js('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/'), Js('slice'), Js('indexOf'), Js(''), Js(''), Js('.'), Js('pow'), Js('reduce'), Js('reverse'), Js('0')]))
pass
pass
pass
