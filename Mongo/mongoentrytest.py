import mongoentry as me

ent = me.SoccerEntry().name("Galaxy").wins2011(10).visualization(None).win_rate_on_rainy_days(.3).goals2011(302)
if ent.ready():
    print(ent.process_entry())
else:
    print("missing some values")
assert ent.ready()

ent2 = me.SoccerEntry().name("Galaxy").wins2011(10).visualization(None).win_rate_on_rainy_days(.3)

assert not ent2.ready()
