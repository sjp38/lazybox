/**
 * stress memory
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>

#define FILEPATH "2000MiB_file"
#define FILE_SIZE ((unsigned long)2 * 1000 * 1024 * 1024) /* 2000 MiB */

#define NR_WORKER 20

#define RW_SIZE (43 * 1024 * 1024)

FILE *fp;
int stop_stress = 0;
int RUNTIME = 10;

static void *random_rw(void *arg)
{
	int offset, read_only, value;
	char *buffer;

	buffer = (char *)malloc(RW_SIZE);

	printf("[worker] start random rw\n");
	while (!stop_stress) {
		offset = rand() % (FILE_SIZE - RW_SIZE);
		fseek(fp, offset, SEEK_SET);

		fread(buffer, sizeof(char), RW_SIZE, fp);

		read_only = rand() % 1;
		if (!read_only) {
			value = rand();
			memset(buffer, value, RW_SIZE);
			fseek(fp, offset, SEEK_SET);
			fwrite(buffer, sizeof(char), RW_SIZE, fp);
		}
	}
	free(buffer);
	printf("[worker] done...\n");
	return 0;
}

int main(int argc, char **argv)
{
	pthread_t worker[NR_WORKER];
	int i;

	if (argc > 1)
		RUNTIME = atoi(argv[1]);

	fp = fopen(FILEPATH, "r+");


	srand(time(NULL));
	for (i = 0; i < NR_WORKER; i++) {
		if (pthread_create(&worker[i], NULL, random_rw, NULL)) {
			fprintf(stderr, "failed to create worker thread!\n");
			exit(1);
		}
	}
	sleep(RUNTIME);
	stop_stress = 1;
	for (i = 0; i < NR_WORKER; i++)
		pthread_join(worker[i], NULL);

	return 0;
}
