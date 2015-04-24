.SUFFIXES: .c .o

CFLAGS	:= -Wall -Werror -g
CC	:= gcc
LIBS	:= -lpthread

OBJS	:= stress.o
TARGET	:= stress

${TARGET} : ${OBJS}
	${CC} ${CFLAGS} -o $@ ${OBJS} ${LIBS}

.c.o :
	${CC} ${CFLAGS} -c $< -o $@ ${LIBS}

clean:
	rm -f ${OBJS} ${TARGET} core

APPS	:= stress
