##--------------------------------------------------------------------------------------------##
##                                 SUJET 1 - PROJET CYBERSECURITE                             ##
##  authors : PRUVOST Jordan, TAKAHASHI Vincent, OUKZIZ Salma, GONAY Arthur & BOUGHAMNI Rami  ##
##                                       date : 27/10/22                                      ##
##--------------------------------------------------------------------------------------------##

#_____________________________________________________________________________________________#

# Build proxy server

import requests as rq

s = rq.session()
s.proxies = {"tap something 'http' & 'https' "}