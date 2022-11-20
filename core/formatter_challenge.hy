;____
(import
  math [ isnan]
  fractions [ Fraction]
  re
  datetime
  collections
  _collections_abc [ dict-keys dict-values dict-items])

;comment_350fcdd6

(setv _registry {})
(defn hy-repr-register [ types f [ placeholder None]]
   string_ceb61d8f
 
  (for [ typ (if (isinstance types list) types [ types])]
    (setv (get _registry typ) #(f placeholder))))

(setv _quoting False)
(setv _seen (set))
(defn hy-repr [ obj]
   string_5b6fd879
 
  (setv [ f placeholder] (.get _registry (type obj) [ _base-repr None]))

  (global _quoting)
  (setv started-quoting False)
  (when (and (not _quoting) (isinstance obj hy.models.Object)
             (not (isinstance obj hy.models.Keyword)))
    (setv _quoting True)
    (setv started-quoting True))

  (setv oid (id obj))
  (when (in oid _seen)
    (return (if (is placeholder None)  string_04e5b492  placeholder)))
  (.add _seen oid)

  (try
    (+ (if started-quoting  string_c286150d   string_26c8a224 ) (f obj))
    (finally
      (.discard _seen oid)
      (when started-quoting
        (setv _quoting False)))))

(hy-repr-register
  [ tuple hy.models.Tuple]
  (fn [ x]
    (+  string_d270d3cd  (_cat x)  string_28cd5ec5 )))

(hy-repr-register dict :placeholder  string_0a1aa2f2  (fn [ x]
  (setv text (.join  string_9571c21d  (gfor
    [ k v] (.items x)
    (+ (hy-repr k)  string_9a953bac  (hy-repr v)))))
  (+  string_5182d690  text  string_eff588fb )))
(hy-repr-register hy.models.Dict :placeholder  string_0a1aa2f2  (fn [ x]
  (setv text (.join  string_9a953bac  (gfor
    [ i item] (enumerate x)
    (+ (if (and i (= (% i 2) 0))  string_9a953bac   string_26c8a224 ) (hy-repr item)))))
  (+  string_5182d690  text  string_eff588fb )))
(hy-repr-register hy.models.Expression (fn [ x]
  (setv syntax { 
    'quote  string_c286150d 
    'quasiquote  string_edab2bbf 
    'unquote  string_5672de53 
    'unquote-splice  string_31195048 
    'unpack-iterable  string_877325fc 
    'unpack-mapping  string_29318953 })
  (cond
    (and x (in (get x 0) syntax))
      (+ (get syntax (get x 0)) (hy-repr (get x 1)))
    True
      (+  string_b775f6f9  (_cat x)  string_28cd5ec5 ))))

(hy-repr-register [ hy.models.Symbol hy.models.Keyword] str)
(hy-repr-register [ hy.models.String str hy.models.Bytes bytes] (fn [ x]
  (setv r (.lstrip (_base-repr x)  string_04fa7aac
  None))
     string_213308e4
 
    (+
      (if (isinstance x bytes)  string_620927a1
 )
      (if (.startswith  string_7cee94a4  r)
        ;comment_a17f482f
        ;comment_2440c7fc
        r
        ;comment_37bd7322
        ;comment_b42bb1bf
        (+  string_7cee94a4  (.replace (cut r 1 -1)  string_7cee94a4   string_a6f2e3eb )  string_7cee94a4 ))))))
(hy-repr-register bytearray (fn [ x]
   string_ae74b963
 ))
(hy-repr-register bool str)
(hy-repr-register [ hy.models.Float float] (fn [ x]
  (setv fx (float x))
  (cond
    (isnan fx)   string_1a9c8de7 
    (= fx Inf)   string_0659505b
 )  string_9a0ab1eb
   string_1a9c8de7 )))

(hy-repr-register [ range slice]
                  (fn [ x]
                    (setv op (. (type x) __name__))
                    (if (= x.step (if (is (type x) range) 1 None))
                        (if (= x.start (if (is (type x) range) 0 None))
                             string_a870bc69
 
                             string_9f5f6873
 )
                         string_967ad7e5
 )))

(hy-repr-register
  hy.models.FComponent
  (fn [ x] (+
     string_5182d690 
    (hy-repr (get x 0))
    (if x.conversion  string_4173d328
   string_26c8a224 )
    (if (> (len x) 1)
      (+  string_ea413af7  (if (isinstance (get x 1) hy.models.String)
        (get x 1)
        (hy-repr (get x 1))))
       string_26c8a224 )
     string_eff588fb )))

(hy-repr-register
  hy.models.FString
  (fn [ fstring]
    (if (is-not None fstring.brackets)
      (+  string_d61bacc6  fstring.brackets  string_8dbb5b2c 
         #* (lfor component fstring
                  (if (isinstance component hy.models.String)
                      (.replace (.replace (str component)
                         string_5182d690   string_daa7f28b )
                         string_eff588fb   string_631dd5ef )
                      (hy-repr component)))
          string_4733db0b  fstring.brackets  string_4733db0b )
      (+  string_c446d563 
         #* (lfor component fstring
                  :setv s (hy-repr component)
                  (if (isinstance component hy.models.String)
                      (.replace (.replace (cut s 1 -1)
                         string_5182d690   string_daa7f28b )
                         string_eff588fb   string_631dd5ef )
                      s))
          string_7cee94a4 ))))

(setv _matchobject-type (type (re.match  string_26c8a224   string_26c8a224 )))
(hy-repr-register _matchobject-type (fn [ x]
  (.format  string_6f1c10bf
 
    _matchobject-type.__module__
    _matchobject-type.__name__
    (hy-repr (.span x))
    (hy-repr (.group x 0)))))
(hy-repr-register re.Pattern (fn [ x]
  (setv flags (& x.flags (~ re.UNICODE)))
    ;comment_f8d5527b
    ;comment_53692f10
  (.format  string_10a04b1b
 
    (hy-repr x.pattern)
    (if flags
      (+  string_9a953bac  (do
        ;comment_e1c87eee
        (setv flags (re.RegexFlag flags))
        (setv flags (lfor
          f (sorted re.RegexFlag)
          :if (& f flags)
          (+  string_86d3aabb  f.name)))
        (if (= (len flags) 1)
          (get flags 0)
          (.format  string_66963223  (.join  string_9a953bac  flags)))))
       string_26c8a224 ))))

(hy-repr-register datetime.datetime (fn [ x]
  (.format  string_0badb381
 
    (_strftime-0 x  string_968f0785
 )
    (_repr-time-innards x))))
(hy-repr-register datetime.date (fn [ x]
  (_strftime-0 x  string_7182029c
 )))
(hy-repr-register datetime.time (fn [ x]
  (.format  string_4b4d7931
 
    (_strftime-0 x  string_5824b6ed )
    (_repr-time-innards x))))
(defn _repr-time-innards [ x]
  (.rstrip (+  string_9a953bac  (.join  string_9a953bac  (filter (fn [ x] x) [ 
    (when x.microsecond (str x.microsecond))
    (when (is-not x.tzinfo None) (+  string_bde8b798  (hy-repr x.tzinfo)))
    (when x.fold (+  string_c761c963  (hy-repr x.fold)))])))))
(defn _strftime-0 [ x fmt]
  ;comment_63f652cb
  ;comment_daae9ff1
  (re.sub  string_d0d7b7a8
   string_9c1fd04d  (.strftime x fmt)))

(hy-repr-register collections.ChainMap (fn [ x]
  (.format  string_e0e65c82
 
    (_cat x.maps))))
(hy-repr-register collections.Counter (fn [ x]
  (.format  string_f93d3ffb
 
    (hy-repr (dict x)))))
(hy-repr-register collections.OrderedDict (fn [ x]
  (.format  string_975c18b5
 
    (hy-repr (list (.items x))))))
(hy-repr-register collections.defaultdict (fn [ x]
  (.format  string_178494bb
 
    (hy-repr x.default-factory)
    (hy-repr (dict x)))))
(hy-repr-register
  Fraction
  (fn [ x]  string_68b32f5b
 ))

(for [ [ types fmt] [ 
    [ [list hy.models.List]  string_2ad22f47 ]
    [ [set hy.models.Set]  string_f42977b2 ]
    [ frozenset  string_0c84e409
 ]
    [ collections.deque  string_8cb4fe59
 ]
    [ dict-keys  string_8014a0d5
 ]
    [ dict-values  string_836555c5
 ]
    [ dict-items  string_bcf5b2ec
 ]]]
  (defn mkrepr [ fmt]
    (fn [ x] (.replace fmt  string_04e5b492  (_cat x) 1)))
  (hy-repr-register types :placeholder fmt (mkrepr fmt)))

(defn _cat [ obj]
  (.join  string_9a953bac  (map hy-repr obj)))

(defn _base-repr [ x]
  (when (and (isinstance x tuple) (hasattr x  string_864dd8cf ))
    ;comment_c01b54fd
    ;comment_7eb6ad5f
    ;comment_e46336d2
    (return (.format  string_4814b242 
                     (. (type x) __name__)
                     (.join  string_9a953bac  (gfor [ k v] (zip x._fields x) (+  string_44c80ac3  k  string_9a953bac  (hy-repr v)))))))

  (when (not (isinstance x hy.models.Object))
    (return (repr x)))
  ;comment_12aad614
  ;comment_2c58fede
  (.__repr__
    (next (gfor
      t (. (type x) __mro__)
      :if (not (issubclass t hy.models.Object))
      t))
    x))

;____
