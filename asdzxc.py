def function(arg2=1, *args, **kwargs):
    print(arg2)
    print(args)
    print(kwargs)

function(1, *(1238792, 12, 123), **{'title': 1012312})