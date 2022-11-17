import sys
try:
    # exit() # dangerous operation. fuck.
    # quit()
    # ...
    sys.exit(1) # normally it will not do shit.
    # nothing will be run. shit.
except Exception as e:
    print("EXCEPTION:", e)
    print("SYSTEM WILL EXIT, but can we do something about it?")

print("RUN AFTER EXIT?")