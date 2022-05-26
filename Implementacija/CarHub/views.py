
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from django.template.defaultfilters import register


from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from .models import *
from json import dumps

from django.http import HttpResponseRedirect


from django import template


# from CarHub.forms import NewUserForm


# Create your views here.

@register.filter
def index(sequence, position):
    return sequence[position]

def Test(request):
    # return HttpResponse("<h1> CarHub doktoriii</h1>")
    return render(request, 'pocetnaStrana.html', {'imeSlike': 'carhublogo.png'})


def Ulogovan(request):
    # return HttpResponse("<h1> CarHub doktoriii</h1>")
    return render(request, 'pocetnaStranaUlogovan.html')



@login_required(login_url='prijava.html')
def profilKorisnika(request):
    trenutni = request.user
    komentar = Komentar.objects.order_by('-timestamp').filter(profilKorisnika=trenutni)
    oceneKorisnika = Ocena.objects.all().filter(korisnik=trenutni)
    ukupnoOcena = Ocena.objects.all().filter(korisnik=trenutni).count()
    ocene1 = 0
    ocene2 = 0
    ocene3 = 0
    ocene4 = 0
    ocene5 = 0

    for o in oceneKorisnika:
        if o.ocena == 1:
            ocene1 = ocene1 + 1
        elif o.ocena == 2:
            ocene2 = ocene2 + 1
        elif o.ocena == 3:
            ocene3 = ocene3 + 1
        elif o.ocena == 4:
            ocene4 = ocene4 + 1
        elif o.ocena == 5:
            ocene5 = ocene5 + 1

    if ukupnoOcena != 0:
        ocene1Bar = ocene1 / ukupnoOcena * 100
        ocene2Bar = ocene2 / ukupnoOcena * 100
        ocene3Bar = ocene3 / ukupnoOcena * 100
        ocene4Bar = ocene4 / ukupnoOcena * 100
        ocene5Bar = ocene5 / ukupnoOcena * 100
    else:
        ocene1Bar = 0
        ocene2Bar = 0
        ocene3Bar = 0
        ocene4Bar = 0
        ocene5Bar = 0
    if ukupnoOcena > 0:
        prosecnaOcena = (ocene1 + ocene2 * 2 + ocene3 * 3 + ocene4 * 4 + ocene5 * 5) / ukupnoOcena
        prosecnaOcena = (round(prosecnaOcena, 2))
        if prosecnaOcena > 2.5:
            if prosecnaOcena < 3.5:
                zvezdice = 3
            elif prosecnaOcena > 4.5:
                zvezdice = 5
            else:
                zvezdice = 4
        else:
            if prosecnaOcena > 1.5:
                zvezdice = 2
            elif prosecnaOcena < 0.5:
                zvezdice = 1
            else:
                zvezdice = 0

    else:
        prosecnaOcena = 0
        zvezdice = 0

    data = []
    for i in range(5):
        data.append(i + 1)

    context = {
        'komentar': komentar,
        'ocene1': ocene1,
        'ocene2': ocene2,
        'ocene3': ocene3,
        'ocene4': ocene4,
        'ocene5': ocene5,
        'ukupnoOcena': ukupnoOcena,
        'prosecnaOcena': prosecnaOcena,
        'ocene1Bar': ocene1Bar,
        'ocene2Bar': ocene2Bar,
        'ocene3Bar': ocene3Bar,
        'ocene4Bar': ocene4Bar,
        'ocene5Bar': ocene5Bar,
        'zvezdice': zvezdice,
        'data': data

    }
    return render(request, 'profilKorisnika.html', context)


def profilDrugogKorisnika(request, korisnik_id):
    profil = Korisnik.objects.get(id=korisnik_id)
    komentar = Komentar.objects.order_by('-timestamp').filter(profilKorisnika=profil)
    oceneKorisnika = Ocena.objects.all().filter(korisnik=profil)

    tempOcena = Ocena.objects.filter(ocenio=request.user, korisnik=profil)

    if oceneKorisnika.filter(ocenio=request.user):
        ocenjen = 1
        ocenaUlogovanog = tempOcena.first().ocena

    else:
        ocenjen = 0
        ocenaUlogovanog = -1

    ukupnoOcena = Ocena.objects.all().filter(korisnik=profil).count()

    if request.method == 'POST':
        form = KomentarForm(request.POST or None)
        if form.is_valid():
            kom = form.save(commit=False)
            kom.autor = request.user
            kom.profilKorisnika = profil
            kom.save()
            return HttpResponseRedirect(request.path_info)
    form = KomentarForm()

    if request.method == "POST":
        rate = request.POST.get('rate')
        if rate is None:
            pass
        else:
            if str(rate) == '1':
                ocena = Ocena(ocena=5, korisnik=profil, ocenio=request.user)
                ocena.save()  # Naopaki su brojevi jer su radioButtoni naopaki
            elif str(rate) == '2':
                ocena = Ocena(ocena=4, korisnik=profil, ocenio=request.user)
                ocena.save()
            elif str(rate) == '3':
                ocena = Ocena(ocena=3, korisnik=profil, ocenio=request.user)
                ocena.save()
            elif str(rate) == '4':
                ocena = Ocena(ocena=2, korisnik=profil, ocenio=request.user)
                ocena.save()
            elif str(rate) == '5':
                ocena = Ocena(ocena=1, korisnik=profil, ocenio=request.user)
                ocena.save()
            else:
                print("greska")
        return HttpResponseRedirect(request.path_info)

    ocene1 = 0
    ocene2 = 0
    ocene3 = 0
    ocene4 = 0
    ocene5 = 0

    for o in oceneKorisnika:
        if o.ocena == 1:
            ocene1 = ocene1 + 1
        elif o.ocena == 2:
            ocene2 = ocene2 + 1
        elif o.ocena == 3:
            ocene3 = ocene3 + 1
        elif o.ocena == 4:
            ocene4 = ocene4 + 1
        elif o.ocena == 5:
            ocene5 = ocene5 + 1

    if ukupnoOcena != 0:
        ocene1Bar = ocene1 / ukupnoOcena * 100
        ocene2Bar = ocene2 / ukupnoOcena * 100
        ocene3Bar = ocene3 / ukupnoOcena * 100
        ocene4Bar = ocene4 / ukupnoOcena * 100
        ocene5Bar = ocene5 / ukupnoOcena * 100
    else:
        ocene1Bar = 0
        ocene2Bar = 0
        ocene3Bar = 0
        ocene4Bar = 0
        ocene5Bar = 0

    if ukupnoOcena > 0:
        prosecnaOcena = (ocene1 + ocene2 * 2 + ocene3 * 3 + ocene4 * 4 + ocene5 * 5) / ukupnoOcena
        prosecnaOcena = (round(prosecnaOcena, 2))
        if prosecnaOcena > 2.5:
            if prosecnaOcena < 3.5:
                zvezdice = 3
            elif prosecnaOcena > 4.5:
                zvezdice = 5
            else:
                zvezdice = 4
        else:
            if prosecnaOcena > 1.5:
                zvezdice = 2
            elif prosecnaOcena < 0.5:
                zvezdice = 1
            else:
                zvezdice = 0
    else:
        prosecnaOcena = 0

    if prosecnaOcena > 2.5:
        if prosecnaOcena < 3.5:
            zvezdice = 3
        elif prosecnaOcena > 4.5:
            zvezdice = 5
        else:
            zvezdice = 4
    else:
        if prosecnaOcena > 1.5:
            zvezdice = 2
        elif prosecnaOcena < 0.5:
            zvezdice = 1
        else:
            zvezdice = 0

    data = []
    for i in range(5):
        data.append(i + 1)

    context = {
        'profil': profil,
        'komentar': komentar,
        'ocene1': ocene1,
        'ocene2': ocene2,
        'ocene3': ocene3,
        'ocene4': ocene4,
        'ocene5': ocene5,
        'ukupnoOcena': ukupnoOcena,
        'prosecnaOcena': prosecnaOcena,
        'ocene1Bar': ocene1Bar,
        'ocene2Bar': ocene2Bar,
        'ocene3Bar': ocene3Bar,
        'ocene4Bar': ocene4Bar,
        'ocene5Bar': ocene5Bar,
        'zvezdice': zvezdice,
        'data': data,
        'form': form,
        'ocenjen': ocenjen,
        'ocenaUlogovanog': ocenaUlogovanog
    }
    return render(request, 'profilDrugogKorisnika.html', context)


@login_required(login_url='login')
def create_Komentar(request):
    form = KomentarForm(request.POST or None)
    if form.is_valid():
        kom = form.save(commit=False)
        kom.autor = Korisnik.objects.get(username=request.user.get_username())
        kom.save()
        return redirect('profilDrugogKorisnika.html')






def konkretanOglasProdaja(request, oglas_id):
    #namestiti
    oglas = Oglas.objects.get(pk = oglas_id)
    model_oglasa = oglas.model_idmodel
    lista_slika = list(Slike.objects.filter(fk_oglas=oglas))
    print(lista_slika[0].slike)
    #slika1 = lista_slika[0]
    oglas_dict = {
        'brend' : model_oglasa.brend,
        'model' : model_oglasa.naziv_modela,
        'cena' : oglas.cena,
        'boost' : oglas.boost,
        'slike' : lista_slika,
        'snaga' : oglas.snaga,
        'kilometraza' : oglas.kilometraza,
        'godiste' : oglas.godiste,
        'karoserija' : oglas.karoserija,
    }

    return render(request, 'konkretanOglasProdaja.html', context={'oglas' : oglas_dict})



def konkretanOglasRent(request):
    #namestiti
    return render(request, 'konkretanOglasRent.html')





def urediProfil(request):
<<<<<<< HEAD
    # try:
    #     profil = Korisnik
    #
    #     context = {    #     }
    return render(request, 'urediProfil.html')


# except Korisnik.DoesNotExist:
#     raise Http404("Korisnik not found")


def postavljanjeOglasa(request):
    forma = PostavljanjeOglasa(request.POST, request.FILES)
=======
    trenutniKorisnik = request.user
    kime = None
    pas = None
    fon = None
    mail = None
    form = PromeniSliku(request.POST or None, request.FILES or None)
    if form.is_valid():
        kime = request.POST['ime1']
        pas = request.POST['sifra1']
        fon = request.POST.get('telefon1')
        mail = request.POST.get('mejl1')
        slika = form.cleaned_data.get('slika')
        if slika is not None:
            trenutniKorisnik.slika = slika

        if len(kime)> 6 :
            trenutniKorisnik.username = kime
        if len(pas) > 6 :
            trenutniKorisnik.set_password(pas)
        if len(fon)> 6 :
            trenutniKorisnik.kontakt_telefon = fon
        if len(mail)> 6 :
            trenutniKorisnik.email = mail
        trenutniKorisnik.save()
    context = {
        "forma_promenaSlike": form
    }

    return render(request, 'urediProfil.html',context = context)




def PretragaOglasa(request):

    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela"))
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])

    forma=pretragaOglasa(request.POST or None)
    if forma.is_valid():
        brend = request.POST['dropdown_Brend']
        naziv_model = request.POST['dropdown_Model']
        godiste1 = forma.cleaned_data.get('godiste1')
        godiste2 = forma.cleaned_data.get('godiste2')
        karoserija = forma.cleaned_data.get('karoserija')
        cenaOd = forma.cleaned_data.get('cena1')
        cenaDo = forma.cleaned_data.get('cena2')

        oglasi = []
        imgs = []
        models_ids = Model.objects.filter(godisteOd__gte=godiste1).filter(godisteDo__lte=godiste2).filter(
            brend=brend).filter(naziv_modela=naziv_model)
        print(models_ids)
        for model in models_ids:
            oglasi.extend(list(Oglas.objects.filter(model_idmodel=model).filter(godiste__lte=godiste2).filter(godiste__gte=godiste1).filter(karoserija=karoserija).filter(cena__gte=cenaOd).filter(cena__lte=cenaDo)))
        print(oglasi)
        for oglas in oglasi:
            nesto = Slike.objects.filter(fk_oglas=oglas)
            imgs.append(nesto.first().slike)
            #imgs.append((Slike.objects.filter(fk_oglas=oglas)).first().slike)
            print(imgs)
        dataJSON = dumps(niz)
        context = {
            "naziv_brenda" : brend,
            "naziv_modela" : naziv_model,
            "slike" : imgs,
            "oglasi" : oglasi,
            "data": dataJSON,
            "brendovi": brendovi,
            "forma_pretraziOglas": forma
        }

        return render(request=request, template_name='pretragaOglasa.html', context = context)





    #ako je korisnik poslat na stranicu pretrage preko get requesta, to znaci da je to prvi ulaz tu,
    #a ako je preko post requesta, onda je vec napravio filtere i primenio ih
    #U slucaju da korisnik dolazi na sajt get requestom, pravi se lista od pocetnih 9 oglasa(boostovani, ili svi boos
    # tovani sa skrolom), a u slucaju da se dolazi na sajt nakon post requesta, onda se primenjuju filteri i
    #salju odgovarajuci oglasi

    #ovde ide kod za dobijanje boostovanih oglasa i njihovo slanje nakon GET request-a

    dataJSON = dumps(niz)
    context = {
        # "slike" : imgs,
        # "oglasi" : oglasi,
        "data": dataJSON,
        "brendovi" : brendovi,
        "forma_pretraziOglas":forma
    }
    return render(request=request, template_name='pretragaOglasa.html', context = context)


def PretragaOglasaRent(request):
    forma=pretragaOglasaRent(request.POST or None)
>>>>>>> main
    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela"))
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])
    # print(niz)
    # print(brendovi_modeli)

    dataJSON = dumps(niz)
    context = {
        "data": dataJSON,
<<<<<<< HEAD
        "brendovi": brendovi,
        "forma_postaviOglas": forma
=======
        "brendovi" : brendovi,
        "forma_pretraziOglasRent":forma
    }
    return render(request=request, template_name='pretragaOglasaRent.html', context = context)


def postavljanjeOglasa(request):
    form=PostavljanjeOglasa(request.POST or None,request.FILES or None)
    if form.is_valid():
        izbor = request.POST['izbor']
        brend = request.POST['dropdown_Brend']
        naziv_model = request.POST['dropdown_Model']
        godiste = form.cleaned_data.get('godiste')
        kilometraza = form.cleaned_data.get('kilometraza')
        snaga = form.cleaned_data.get('snagaMotora')
        karoserija = form.cleaned_data.get('karoserija')
        slike = request.FILES.getlist('images')

        model_id = Model.objects.filter(godisteOd__lte=godiste).filter(godisteDo__gte=godiste).filter(
            brend=brend).filter(naziv_modela=naziv_model)  #filtriranje radi pronalaska id-ja modela
        #print(model_id)
        #proveriti sta vraca post request za izbor (da li vraca value od pritisnitog dugmeta)
        if (izbor == "prodaja"):
            cena = request.POST["cenaProdaja"];
            for img in slike:
                print(img)
            oglas = Oglas(tip = "p", cena = cena, boost = 0, grad = '', slike = slike,
                          snaga = snaga, kilometraza=kilometraza, karoserija=karoserija,
                          godiste=godiste, model_idmodel=model_id.first())
            oglas.save()
            for img in slike:
                photo = Slike.objects.create(slike = img, fk_oglas = oglas)
        else:
            pass
        #napraviti razlicite ifove za prodaju i iznajmljivanje
        #ako je prodaja, moze odmag da se postavi oglas
        #ako je iznajmljivanje, treba smisliti nacin za kupljenje datuma i za njihovubacivanje u bazu
        #takodje, mora se naci id_Modela pomocu brenda, modela i godista

    brendovi = Model.objects.values("brend").distinct()
    brendovi_modeli = list(Model.objects.values("brend", "naziv_modela"))
    niz = []
    for model in brendovi_modeli:
        niz.append([str(model["brend"]), str(model["naziv_modela"])])
    # print(niz)
    # print(brendovi_modeli)

    dataJSON = dumps(niz)
    context = {
        "data": dataJSON,
        "brendovi" : brendovi,
        "forma_postaviOglas":form
>>>>>>> main
    }
    return render(request=request, template_name='testForme.html', context=context)




def registracija(request):
    form = KorisnikNoviForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("CarHub:pocetnaStranaUlogovan")

    form = KorisnikNoviForm()
    return render(request=request, template_name="registracijaProbaDjango.html", context={"register_form": form})
    # return render(request,"registracijaProbaDjango.html")

<<<<<<< HEAD

def pretragaOglasa(request):
    return render(request, 'pretragaOglasa.html')


def pregledOglasa(request):
    return render(request, 'pregledOglasa.html')

=======
>>>>>>> main

def prijava(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)  # moraju da se taguju
            if user is not None:
                login(request, user)
                messages.info(request, f"Ulogovani ste kao{username}.")
                return redirect("CarHub:pocetnaStranaUlogovan")
            else:
                messages.error(request, "Netacno ime ili lozinka.")
        else:
            messages.error(request, "Netacno ime ili lozinka.")
    form = AuthenticationForm()
    return render(request=request, template_name="prijavaProbaDjango.html", context={"login_form": form})


            

def logout(request):
    messages.info(request, "Uspesno ste izlogovani")
    return redirect("CarHub:pocetnaStrana")
