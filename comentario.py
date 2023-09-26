from enum import Enum
import re

class Classificacao(Enum):
    Negativo = 0
    Neutro = 1
    Positivo = 2

class Comentario:
    tipo: Classificacao
    txt: str

    def __init__(self, tipo, txt):
        self.tipo = tipo
        self.txt = txt

class AnalisadorComentario:
    __palavras_positivas = "(baita filme)|(lindo)|(adoro)|(bom)|(otim)|(incrível)|(maravilhoso)|(divertido)|(emocionante)|(ótimo)|(excelente)|(adorei)|(surpre)|(cativante)|(supimpa)|(excelente)|(incrivel)|(maravilh)|(fantastic)|(brilh)|(espetacular)|(surpreend)|(impression)|(fenomenal)|(diverti)|(emocion)|(cativ)|(envolv)|(notavel)|(genial)|(formidavel)|(extraordinario)|(encant)|(estupendo)|(estonteante)|(inigualável)|(perfeito)|(magistral)|(impecavel)|(inovador)|(inesquecivel)|(inspir)|(ótimo)|(esplendido)|(melhor)|(incomparavel)|(fenomenal)|(imensamente)|(notavelmente) |(sublime)|(deslumbr)|(adorei)|(amei)|(gostei)|(divert)|(emocionante)|(cativante)|(sens)|(extrao)|(espetac)|(perfe)|(admir)|(envolven)|(inov)|(inesquecivel)|(impact)|(amei)|(top)|(obra-prima)|(obra prima)|(epico)|(magnifico)|(excepcional)|(imperdivel)|(maior filme)|(foda)"
    __palavras_negativas = "(péssimo)|(fraco)|(não gostei)|(não recomendo)|(terrível)|(detestei)|(chato)|(irritante)|(ruim)|(insatisfatório)|(nao gostei)|(irrit)|(ruim)|(terrivel)|(horrivel)|(pessimo)|(desagradavel)|(desastroso)|(detestavel)|(aborrecido)|(desanimador)|(cansativo)|(chato)|(lamentavel)|(triste)|(decepcionante)|(frustrante)|(desapontador)|(desgostoso)|(desprezivel)|(desastroso)|(irritante)|(desconfortavel)|(desagradavel)|(desinteressante)|(odioso)|(insatisfatorio)|(desfavoravel)|(mau)|(negativo)|(prejudicial)|(destrutivo)|(inaceitavel)|(incompreensivel)|(injusto)|(inconveniente)|(insuportavel)|(infernal)|(infeccioso)|(infeliz)|(miseravel)|(tragico)|(desgostoso)|(desalentador)|(indesejavel)|(desfavoravel)|(lamentavel)|(dificil)|(doloroso)|(agonizante)|(incomodo)|(incomodo)|(debil)|(patetico)|(horrendo)|(nefasto)|(repugnante)|(tenebroso)|(desonesto)|(cruel)|(abominavel)|(atroz)|(perverso)|(malevolo)|(repulsivo)|(infame)|(lixo)|(incel)|(incoerente)|(nojo)|(pior)|(frac)|(incoeren)|(entediante)|(nexo)|(cansativo)|(bosta)|(previsível)|(decep)|(repetitivo)|(lacraçao)|(generico)|(esquec)|(porcaria)|(horroroso)"
    id = ''
    txt = ''
    comentarios: list[Comentario] = []
    
    def analisaPalavras(self):
        comentarios = open(self.id, "r", encoding="utf-8")
        pos = 0
        neg = 0
        for i in comentarios:
            if(i != '\n' and i.startswith('_')):
                if(re.findall(self.__palavras_negativas, i.lower()) != list()):
                    neg = self.contador(self.__palavras_negativas, i.lower())
                if(re.findall(self.__palavras_positivas, i.lower()) != list()):
                    pos = self.contador(self.__palavras_positivas, i.lower())
                
                if(neg > pos):
                    print("Comentário Negativo: "+i)
                    x = Comentario(Classificacao.Negativo, i)
                    self.comentarios.append(x)
                elif(pos > neg):
                    print("Comentário Positivo: "+i)
                    x = Comentario(Classificacao.Positivo, i)
                    self.comentarios.append(x)
                else:
                    print("Comentário Neutro: "+i)
                    x = Comentario(Classificacao.Neutro, i)
                    self.comentarios.append(x)
            pos = 0
            neg = 0

    def contador(self, r, t):
        x = 0
        lista = re.findall(r, t)
        for i in lista:
            if(i != ''): x += 1
        return x

    def salvarArquivo(self, p, n, n2):
        arq_saida = open('classificacao_'+self.id, 'w', encoding='utf-8')
        for comentario in self.comentarios:
            if(comentario.tipo == Classificacao.Positivo):
                arq_saida.write('Comentário Positivo: '+comentario.txt[1:] + '\n\n')
            elif(comentario.tipo == Classificacao.Negativo):
                arq_saida.write('Comentário Negativo: '+comentario.txt[1:] + '\n\n')
            else:
                arq_saida.write('Comentário Neutro: '+comentario.txt[1:] + '\n\n')
        arq_saida.write('Análise final:\nPositivos: '+str(p)+'%\nNegativos: '+str(n)+'%\nNeutros: '+str(n2)+'%')
        arq_saida.close()

    def calculaPercentual(self):
        positivo = 0
        negativo = 0
        neutro = 0
        for i in self.comentarios:
            if(i.tipo == Classificacao.Positivo):
                positivo += 1
            elif(i.tipo == Classificacao.Negativo):
                negativo += 1
            else:
                neutro += 1
        total = neutro + negativo + positivo
        pPositivo = (positivo/total)*100
        pNegativo = (negativo/total)*100
        pNeutro = (neutro/total)*100
        print('Análise final:'+str(pPositivo)+'% positivos, '+str(pNegativo)+'% negativos, '+str(pNeutro)+'% neutros')
        self.salvarArquivo(pPositivo, pNegativo, pNeutro)

        

