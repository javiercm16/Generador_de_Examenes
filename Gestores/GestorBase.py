import pymysql
from Modelo.ObjetoItem import ObjetoItem
from Modelo.ObjetoSubtema import ObjetoSubtema
from Modelo.ObjetoTema import ObjetoTema
from Modelo.ObjetoTipoExamen import ObjetoTipoExamen
from Modelo.ObjetoPeriodo import ObjetoPeriodo
from Modelo.ObjetoUsuario import ObjetoUsuario
from Modelo.ObjetoRespuesta import ObjetoRespuesta
from Modelo.ObjetoEncabezado import ObjetoEncabezado
from Modelo.ObjetoVerificacionSugerencia import ObjetoVerificacionSugerencia
from Gestores import GestorExamenes

#TODO AGREGAR A LA SECCION DE ENCABEZADO (BASE Y SISTEMA), LA OPCION DE METER ESCUELA Y CURSO.
#TODO AGREGAR FUNCIONES PARA CARGAR TODOS LOS ENCABEZADOS(PLANTILLAS) Y QUE SEAN EDITABLES Y QUE ESTOS SEAN PREVISUALIZADOS POR EL USUARIO.
#TODO EN UN FUTURO, QUE LE PUEDA CAMBIAR EL TEMA ASOCIADO A UN SUBTEMA,AHORITA SI SE EQUIVOCA DI QUE LO BORRE.
#TODO EN UN FUTURO, QUE LE PUEDA CAMBIAR EL SUBTEMA ASOCIADO A UN ITEM,AHORITA SI SE EQUIVOCA DI QUE LO BORRE.
#TODO ACOMODAR UN POCO EL CODIGO
#TODO VER SI HAY UNA MEJOR MANERA PARA MANEJAR LOS USUARIOS Y HACER QUE EL ACCESO AL CONTROLADOR SEA SINCRONIZADO.
#TODO Buscar cualquier uso que se haga de arreglos en un for y dejar setteado el valor que corresponde mediante loop.index0
#TODO QUITAR LO DE AM Y PM DEL INPUT DE TIPO TIME.

#TODO VER LO DEL API DEL GMAIL PARA ENVIAR CORREO
#TODO CAMBIAR CAMPOS EN LA BASE DE DATOS EN LA PARTE DEL EXAMEN. GUARDAR EN UN CAMPO EL ARCHIVO DEL EXAMEN SOLO SI ESTE ES UN EXAMEN COMPLETO.
#TODO HACER EN LA PARTE DE FILTRADO QUE SE DESCARGUE EL EXAMEN EN FORMATO PDF.
#TODO VALIDACIONES, CAMPOS COMPLETOS, MOSTRAR MENSAJES DE EXITO.
#TODO REVISAR LOS MODALS, QUE ESTAN MEDIOS DESPICHADOS, ACOMODAR PARA QUE LA INFO SALGA ACACHETIN
#TODO VER LO DE LOS BORRADORES


#FUNCIONES DE CONEXION Y QUERIES

def establecerConexion(usuario,password):#usuario,password):

    try:
        return pymysql.connect(host = '127.0.0.1', user = usuario, password = password, db = 'db_exam_it1')
    except Exception as e:

        print("Error de Conexión ",e)

        return False

def obtenerInformacionItem(idItem,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)
    objetoItem = ""
    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as infoItem:
                queryItem = "SELECT id, descripcion, tipo,puntaje FROM Item WHERE idItem = %s"
                infoItem.execute(queryItem,(idItem))

                for atributos in infoItem:
                    objetoItem = ObjetoItem(idItem,atributos[0],atributos[1],atributos[2], None,atributos[3],None)
        except:
            print("Error al obtener la informacion del item")
        finally:
            nuevaConexion.close()
    return objetoItem

def cerrarConexion(objetoConexion):
    objetoConexion.close()

def cargarUsuarios(usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)
    listaUsuarios = []
    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as usuarios:
                queryUsuarios = "SELECT nombreCompleto, correo FROM USUARIO WHERE correo != %s"

                usuarios.execute(queryUsuarios,(usuario))

                for atributos in usuarios:
                    nuevoUsuario = ObjetoUsuario(atributos[0],atributos[1])
                    listaUsuarios += [nuevoUsuario]

        except:
            print("Error al cargar los usuarios.")

        finally:
            nuevaConexion.close()

    return listaUsuarios

def cargarPeriodoExamenes(usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)
    listaPeriodos = []
    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as periodos:

                queryPeriodos = "SELECT id, descPeriodo FROM PERIODO"

                periodos.execute(queryPeriodos)

                for atributos in periodos:
                    nuevoPeriodo = ObjetoPeriodo(atributos[0],atributos[1])

                    listaPeriodos+= [nuevoPeriodo]

        except:
            print("Error al cargar los periódos de examen")

        finally:
            nuevaConexion.close()

    return listaPeriodos

def cargarTipoExamenes(usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    listaTipos=[]

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as  tipoexamenes:
                queryTipos = "SELECT id, descTipo FROM TipoExamen"
                tipoexamenes.execute(queryTipos)

                for atributos in tipoexamenes:
                    nuevoTipoExamen = ObjetoTipoExamen(atributos[0],atributos[1])
                    listaTipos+= [nuevoTipoExamen]
        except:
            print("Error al cargar los periódos de examen")
        finally:
            nuevaConexion.close()

    return listaTipos

def cargarTemas(usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    listaTemas = []

    if (nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as  temas:
                queryTemas = "SELECT id, tema FROM Tema"
                temas.execute(queryTemas)

                for atributos in temas:
                    nuevoTema = ObjetoTema(atributos[0],atributos[1])
                    listaTemas += [nuevoTema]
        except:
            print("Error al cargar los temas de estudio")
        finally:
            nuevaConexion.close()

    return listaTemas

def filtrarSubtemas(idTema,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    listaSubtemas = []

    if (nuevaConexion != False):
        try:
            with nuevaConexion.cursor() as  subtemas:
                querySubtemas = "SELECT id, subtema FROM SubTema WHERE idTema = %s"
                subtemas.execute(querySubtemas,(idTema))

                for atributos in subtemas:
                    nuevoSubtema = ObjetoSubtema(atributos[0],atributos[1],idTema)
                    listaSubtemas += [nuevoSubtema]
        except:
            print("Error al filtrar los subtemas de estudio")
        finally:
            nuevaConexion.close()

    return listaSubtemas

def filtrarItems(idSubtema,tipoFiltrado,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    listaItems = []

    if (nuevaConexion != False):
        try:
            with nuevaConexion.cursor() as items:
                queryitemsTotal = "SELECT idItem,id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s"
                queryitemsUser = "SELECT idItem,id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s AND" \
                                 " usuarioCreador = %s"
                queryitemsNotUser = "SELECT idItem,id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s AND" \
                                 " usuarioCreador != %s"

                if(tipoFiltrado == "total"):
                    items.execute(queryitemsTotal, (idSubtema))
                elif(tipoFiltrado =="parcial"):
                    items.execute(queryitemsUser, (idSubtema, usuario))
                else:
                    items.execute(queryitemsNotUser, (idSubtema, usuario))

                for atributos in items:
                    nuevoItem = ObjetoItem(atributos[0], atributos[1],atributos[2],atributos[3],idSubtema,atributos[4],atributos[5])
                    listaItems += [nuevoItem]
        except:
            print("Error al filtrar los items")
        finally:
            nuevaConexion.close()

    return listaItems

def filtrarItemsRespuestas(idSubtema, tipoFiltrado, usuario, contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)
    listaItems = []

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as itemsRespuestas:
                querySinRespuestas = "SELECT idItem,id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s AND idItem NOT IN (SELECT idItem FROM Respuestas)"
                queryConRespuestas = "SELECT idItem,id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s AND idItem IN (SELECT idItem FROM Respuestas)"

                itemsRespuestas.execute(querySinRespuestas,(idSubtema)) if tipoFiltrado == "SinResp" else  itemsRespuestas.execute(queryConRespuestas,(idSubtema))

                for atributos in itemsRespuestas:
                    nuevoItem = ObjetoItem(atributos[0], atributos[1],atributos[2],atributos[3],idSubtema,atributos[4],atributos[5])
                    listaItems += [nuevoItem]

        except Exception as e:
            print(e)
            print("Error al obtener los items")

        finally:
            nuevaConexion.close()

    return listaItems

def filtrarItemsSeleccion(idSubtema,usuario,contrasenna): #FIXME Not in use
    nuevaConexion = establecerConexion(usuario,contrasenna)
    listaItemsSeleccion = []

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as itemsSelect:

                queryItems = "SELECT idItem,id, descripcion,tipo, puntaje, indiceDiscriminacion FROM Item WHERE idSubtema = %s AND tipo = 'S' "

                itemsSelect.execute(queryItems,(idSubtema))

                for atributos in itemsSelect:
                    listaItemsSeleccion+= [ObjetoItem(atributos[0],atributos[1],
                                                      atributos[2],atributos[3],idSubtema,atributos[4],atributos[5])]

        except:
            print("Error al filtrar los ítems de selección única")
        finally:
            nuevaConexion.close()
    return listaItemsSeleccion

def cargarEncabezados(usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)
    listaEncabezados = []
    if(nuevaConexion !=False):

        try:
            with nuevaConexion.cursor() as encabezados:
                queryEncabezados = "SELECT Encabezado.id, curso, escuela,instrucciones,anno,tiempo," \
                                   "Periodo.id,descPeriodo,TipoExamen.id,descTipo FROM Encabezado,Periodo," \
                               "TipoExamen WHERE idPeriodo = Periodo.id AND idtipoexamen = TipoExamen.id"
                encabezados.execute(queryEncabezados)

                for atributos in encabezados:
                    listaEncabezados.append(ObjetoEncabezado(atributos[0],atributos[1],atributos[2],atributos[3],atributos[4],
                                                             atributos[5],str(atributos[6])+"-"+atributos[7],str(atributos[8])+"-"+atributos[9]))

        except Exception as e:
            print(e)
            print("Error al obtener los encabezados")
        finally:
            nuevaConexion.close()

    return listaEncabezados

#AQUI EMPIEZA EL CRUD DE ENCABEZADO
def agregarEncabezado(objetoEncabezado,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as nuevoEncabezado:
                insertEncabezado = "INSERT INTO Encabezado (curso,escuela,instrucciones,anno,tiempo,idPeriodo,idTipoExamen) VALUES(%s, %s,%s, %s, %s, %s, %s)"
                nuevoEncabezado.execute(insertEncabezado,(objetoEncabezado.getCurso(),objetoEncabezado.getEscuela(),
                                                          objetoEncabezado.getInstrucciones(),objetoEncabezado.getAnno(),
                                                          objetoEncabezado.getTiempo(),objetoEncabezado.getIdPeriodo(),
                                                          objetoEncabezado.getIdTipoExamen()))
                nuevaConexion.commit()
        except:
            print("Error al agregar un nuevo encabezado.")

        finally:
            nuevaConexion.close()

#AQUI EMPIEZA EL CRUD TEMAS SUBTEMAS
def agregarTema(nuevoTemaIngresado,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    if(nuevaConexion != False):
        try:
            with nuevaConexion.cursor() as nuevoTema:

                insertTema = "INSERT INTO Tema (tema) VALUES(%s)"
                nuevoTema.execute(insertTema,(nuevoTemaIngresado))
                nuevaConexion.commit()
        except :

            print("Error al agregar un nuevo tema")
        finally:
            nuevaConexion.close()

def agregarSubtema(nuevoObjetoSubtema,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)

    if(nuevaConexion != False):
        try:
            with nuevaConexion.cursor() as nuevoSubtema:
                insertSubtema = "INSERT INTO Subtema (subtema,idTema) VALUES (%s,%s)"
                nuevoSubtema.execute(insertSubtema,(nuevoObjetoSubtema.getSubtema(),
                                                    nuevoObjetoSubtema.getIdTema()))
                nuevaConexion.commit()
        except:
            print("Error al agregar un nuevo subtema")
        finally:
            nuevaConexion.close()

def modificarTema(objetoModTema,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as temaModificar:

                updateTema = "UPDATE Tema set tema = %s WHERE id = %s"
                temaModificar.execute(updateTema,(objetoModTema.getTema(),
                                                  objetoModTema.getId()))
                nuevaConexion.commit()
        except:
            print("Error al modificar el tema")

        finally:
            nuevaConexion.close()

def eliminarTema(idTema,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    if (nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as temaEliminar:

                deleteTema = "DELETE FROM Tema WHERE id = %s"
                temaEliminar.execute(deleteTema, (idTema))
                nuevaConexion.commit()
        except:
            print("Error al eliminar el tema")

        finally:
            nuevaConexion.close()

def modificarSubtema(objetoModSubtema,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)

    if (nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as subtemaModificar:
                modifySubtema = "UPDATE Subtema SET subtema = %s WHERE id = %s"
                subtemaModificar.execute(modifySubtema, (objetoModSubtema.getSubtema(),
                                                         objetoModSubtema.getId()))
                nuevaConexion.commit()
        except:
            print("Error al modificar el subtema")
        finally:
            nuevaConexion.close()

def eliminarSubtema(idSubtema,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as subtemaEliminar:
                deleteSubtema = "DELETE FROM Subtema WHERE id = %s"
                subtemaEliminar.execute(deleteSubtema, (idSubtema))
                nuevaConexion.commit()
        except:
            print("Error al eliminar el subtema")
        finally:
            nuevaConexion.close()

#AQUI EMPIEZA EL CRUD DE ITEMS
def agregarItem(nuevoObjetoItem,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)

    if(nuevaConexion != False):
        try:
            with nuevaConexion.cursor() as nuevoItem:

                insertItem = "INSERT INTO Item (id, descripcion,tipo,idSubtema,puntaje,usuarioCreador) VALUES(%s,%s,%s,%s,%s,%s)"
                nuevoItem.execute(insertItem,(nuevoObjetoItem.getIdLargo(),nuevoObjetoItem.getDescripcion(),
                                  nuevoObjetoItem.getTipo(),nuevoObjetoItem.getIdSubtema(),nuevoObjetoItem.getPuntaje(),usuario
                                              ))
                nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al agregar un nuevo item")
        finally:
            nuevaConexion.close()

def modificarItem(objetoModItem,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)

    if(nuevaConexion != False):
        try:

            with nuevaConexion.cursor() as itemModificar:

                updateItem = "UPDATE Item SET id = %s, descripcion = %s, tipo = %s, puntaje = %s WHERE idItem =%s"
                itemModificar.execute(updateItem,(objetoModItem.getIdLargo(),objetoModItem.getDescripcion(),objetoModItem.getTipo(),
                                                  objetoModItem.getPuntaje(),objetoModItem.getId()))
                nuevaConexion.commit()

        except Exception as e:
            print(e)
            print("Error al modificar el item")

        finally:
            nuevaConexion.close()

def eliminarItem(idItem,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    if (nuevaConexion != False):
        try:

            with nuevaConexion.cursor() as itemEliminar:

                deleteItem = "DELETE FROM Item WHERE idItem = %s"
                itemEliminar.execute(deleteItem, (idItem))
                nuevaConexion.commit()

        except:
            print("Error al eliminar el item")

        finally:
            nuevaConexion.close()

#AQUI EMPIEZA EL CRUD DE RESPUESTAS

def obtenerIdFilaRespuestas(idItem,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)
    idExtraido = ""
    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as idExtraer:
                queryID = "SELECT id FROM Respuestas WHERE idItem = %s LIMIT 1"
                idExtraer.execute(queryID,(idItem))

                for atributos in idExtraer:
                    idExtraido = atributos[0]
        except:
            print("Error al extraer el id")
        finally:
            nuevaConexion.close()

    return idExtraido

def agregarRespuestas(objetoRespuesta,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)
    cont = 1
    if (nuevaConexion != False):
        try:
            with nuevaConexion.cursor() as nuevaRespuesta:
                for newResp in objetoRespuesta.getRespuestas():
                    insertRespuesta = "INSERT INTO Respuestas (idItem, respuesta,respuestaCorrecta) VALUES(%s,%s,%s)"
                    nuevaRespuesta.execute(insertRespuesta, (objetoRespuesta.getIdItem(), newResp,"S")) if cont == objetoRespuesta.getRespuestaCorrecta() else nuevaRespuesta.execute(insertRespuesta, (objetoRespuesta.getIdItem(), newResp,"N"))

                    nuevaConexion.commit()
                    cont+=1
        except Exception as e:
            print(e)
            print("Error al agregar una nueva respuesta")
        finally:
            nuevaConexion.close()

def filtrarRespuestasViejas(idItem,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)
    objetoRespuesta = ObjetoRespuesta(idItem,[],None)
    if (nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as respViejas:

                queryRespuestas = "SELECT respuesta,respuestaCorrecta FROM Respuestas WHERE idItem = %s"

                respViejas.execute(queryRespuestas,(idItem))
                listaRespuestas =[]
                contador =1
                for atributos in respViejas:
                    if(atributos[1] == "S"):
                        objetoRespuesta.respCorrecta = contador
                    contador+= 1

                    listaRespuestas+= [atributos[0]]
                objetoRespuesta.respuestas = listaRespuestas

        except:
            print("Error al obtener las respuestas del item")
        finally:
            nuevaConexion.close()

    return objetoRespuesta

def modificarRespuestas(objetoModRespuesta,usuario,contrasenna):
    idFila = obtenerIdFilaRespuestas(objetoModRespuesta.getIdItem(),usuario,contrasenna)
    ids = [idFila+i for i in range(0,4)]

    nuevaConexion = establecerConexion(usuario,contrasenna)

    if (nuevaConexion != False):
        try:
            with nuevaConexion.cursor() as respuestaModificar:

                contador = 1
                index = 0
                for modResp in objetoModRespuesta.getRespuestas():

                    modifyRespuesta = "UPDATE Respuestas SET respuesta = %s, respuestaCorrecta = %s WHERE id = %s"
                    respuestaModificar.execute(modifyRespuesta, (modResp,"S",
                                                             ids[index])) if contador == objetoModRespuesta.getRespuestaCorrecta() else respuestaModificar.execute(modifyRespuesta, (modResp,"N",
                                                             ids[index]))
                    contador+=1
                    index+=1
                    nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al modificar una respuesta")
        finally:
            nuevaConexion.close()

#AQUI EMPIEZA EL CRUD DE INDICE DE DISCRIMINACION

def modificarIndice(objetoModIndice,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)

    if (nuevaConexion != False):
        try:
            with nuevaConexion.cursor() as indiceModificar:

                modifyIndice = "UPDATE Item SET indiceDiscriminacion = %s WHERE idItem = %s"
                indiceModificar.execute(modifyIndice, (objetoModIndice.getIndice(), objetoModIndice.getId()))
                nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al modificar el indice")
        finally:
            nuevaConexion.close()

def eliminarIndice(idItem,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    if (nuevaConexion != False):
        try:
            with nuevaConexion.cursor() as indiceEliminar:

                deleteIndice = "UPDATE Item SET indiceDiscriminacion = NULL WHERE idItem = %s"
                indiceEliminar.execute(deleteIndice, (idItem))
                nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al eliminar el indice")
        finally:
            nuevaConexion.close()

#AQUI EMPIEZA EL SUGERIR-VERIFICAR EDICIONES

def enviarSugerencia(objetoSugerencia, contrasenna):
    nuevaConexion = establecerConexion(objetoSugerencia.getUsuario(),contrasenna)

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as envioSugerencia:
                envioSugerenciaQuery = "INSERT INTO SugerenciaEdicion (idItem,sugerencia,comentarios,usuarioSugeridor) VALUES " \
                                       "(%s,%s,%s,%s)"
                envioSugerencia.execute(envioSugerenciaQuery,(objetoSugerencia.getIdItem(),objetoSugerencia.getSugerencia(),
                                                              objetoSugerencia.getComentarios(),objetoSugerencia.getUsuario()))

                nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al agregar una sugerencia")

        finally:
            nuevaConexion.close()

def filtrarSugerencias(usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)
    objetoSugerenciasVerificar = []
    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as sugerencias:

                querySugerencias = "SELECT Item.idItem, Item.id,Item.descripcion,Item.tipo, Item.puntaje, tema,subtema,sugerencia,comentarios," \
                                   "SugerenciaEdicion.id,Usuario.nombreCompleto" \
                                   " FROM Item,Subtema,Tema,SugerenciaEdicion,Usuario WHERE " \
                                   "Item.idSubtema = Subtema.id AND  Subtema.idTema = Tema.id AND Item.idItem = SugerenciaEdicion.idItem AND " \
                                   "SugerenciaEdicion.aprobacion IS NULL AND SugerenciaEdicion.usuarioSugeridor = Usuario.correo AND " \
                                   "Item.usuarioCreador = %s"
                sugerencias.execute(querySugerencias,(usuario))

                for atributos in sugerencias:
                    objetoSugerenciasVerificar.append(ObjetoVerificacionSugerencia(atributos[0],atributos[1],atributos[2],
                                                                                   atributos[3],atributos[4],atributos[5],atributos[6],
                                                                                   atributos[7],atributos[8],atributos[9],atributos[10]))
        except Exception as e:
            print(e)
            print("Error al obtener las sugerencias")

        finally:
            nuevaConexion.close()

    return objetoSugerenciasVerificar

def aprobarSugerencia(idSugerencia,sugerencia,idItem,usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario, contrasenna)

    if (nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as aprobarSugerencia:
                queryAprobar = "UPDATE SugerenciaEdicion SET aprobacion = 'A' WHERE id = %s"
                queryUpdateItem = "UPDATE Item SET descripcion = %s WHERE idItem = %s"

                aprobarSugerencia.execute(queryAprobar, (idSugerencia))
                aprobarSugerencia.execute(queryUpdateItem,(sugerencia,idItem))

                nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al rechazar la sugerencia")

        finally:
            nuevaConexion.close()

def rechazarSugerencia(idSugerencia,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as rechazarSugerencia:
                queryRechazar = "UPDATE SugerenciaEdicion SET aprobacion = 'R' WHERE id = %s"
                rechazarSugerencia.execute(queryRechazar,(idSugerencia))

                nuevaConexion.commit()
        except Exception as e:
            print(e)
            print("Error al rechazar la sugerencia")

        finally:
            nuevaConexion.close()

#AQUI EMPIEZA CONSTRUIR EXAMEN

def loadInformacionGenerarExamen(tipoExamen,usuario,contrasenna):

    nuevaConexion = establecerConexion(usuario,contrasenna)

    temas= []

    subtemas =[]

    items = []

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as infoExamen:

                queryInformacion ="SELECT Tema.id,Tema.tema,Subtema.id, Subtema.subtema, Item.idItem, Item.id, " \
                                      "Item.descripcion,Item.tipo,Item.puntaje FROM Tema left join Subtema on Tema.id = Subtema.idTema " \
                                      "left join Item on Subtema.Id = Item.idSubtema WHERE Subtema.id is NOT NULL AND Item.idItem is NOT NULL AND Item.tipo =%s "

                infoExamen.execute(queryInformacion,(tipoExamen))

                respuestaTuplas = list(infoExamen.__dict__['_rows'])

                tuplaInfoTema = GestorExamenes.informacionExamen(respuestaTuplas)
                temas += tuplaInfoTema[0]
                subtemas += (tuplaInfoTema[1])
                items += tuplaInfoTema[2]

        except Exception as e:
            print(e)
            print("Error al obtener la información de examen")

        finally:
            nuevaConexion.close()

    return temas,subtemas,items

def guardarExamen(objetoExamen, usuario, contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)

    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as guardarExamen:
                guardarExamenStatement = "INSERT INTO Examen (idEncabezado,modalidadExamen,fechaCreacion,usuarioCreador,archivoExamen) VALUES " \
                                   "(%s, %s, %s, %s, %s)"
                guardarItemsStatement = "INSERT INTO ItemsExamen VALUES(%s, %s)"

                guardarExamen.execute(guardarExamenStatement,(objetoExamen.getEncabezado(),objetoExamen.getModalidadExamen(),
                                                        objetoExamen.getFechaCreacion(),objetoExamen.getCreador(),
                                                        objetoExamen.getArchivoExamen()))
                idExamen = guardarExamen.lastrowid

                tuplasItemsExamen = [(idExamen,idItem) for idItem in objetoExamen.getItems()]
                guardarExamen.executemany(guardarItemsStatement,tuplasItemsExamen)

        except Exception as e:
            print(e)
            print("Error al guardar el examen")

        finally:
            nuevaConexion.close()

#Funciones Correo

def getNombreUsuario(usuario,contrasenna):
    nuevaConexion = establecerConexion(usuario,contrasenna)
    nombreUsuario = ""
    if(nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as nombreCompleto:

                queryNombreCompleto = "SELECT nombreCompleto FROM Usuario WHERE correo = %s"

                nombreCompleto.execute(queryNombreCompleto,(usuario))

                for atributos in nombreCompleto:
                    nombreUsuario = atributos[0]

        except Exception as e:
            print(e)
            print("Error al obtener el nombre del usuario")

        finally:
            nuevaConexion.close()

    return nombreUsuario

def ObtenerPromSubtema(usuario,contrasenna,idSubtema):
    nuevaConexion = establecerConexion(usuario,contrasenna)
    promedio= 0

    if (nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as Consulta:

                queryNombreCompleto = "SELECT AVG(indiceDiscriminacion) FROM item WHERE idSubtema = %s"

                Consulta.execute(queryNombreCompleto, (idSubtema))

                for atributos in Consulta:
                    promedio = atributos[0]

        except Exception as e:
            print(e)
            print("Error al obtener el promedio de Indice de Discriminación de Subtema")

        finally:
            nuevaConexion.close()

    return promedio

def ObtenerCantVecesItem(usuario,contrasenna,idItem):
    nuevaConexion = establecerConexion(usuario,contrasenna)
    cant= 0

    if (nuevaConexion != False):

        try:
            with nuevaConexion.cursor() as Consulta:

                queryNombreCompleto = "SELECT COUNT(*) FROM itemsexamen WHERE itemsexamen.idItem = %s"

                Consulta.execute(queryNombreCompleto, (idItem))

                for atributos in Consulta:
                    cant = atributos[0]

        except Exception as e:
            print(e)
            print("Error al obtener el cantidad de veces usado el item")

        finally:
            nuevaConexion.close()

    return cant

