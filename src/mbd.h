// vim: set ft=c:

extern const _Bool cmbd_with_scalapack;

struct cmbd_calc {
    int n_freq;
    double* omega_grid;
    double* omega_grid_w;
};

struct cmbd_calc* cmbd_init_calc(int n_freq);
void cmbd_set_parallel(struct cmbd_calc* calc);
void cmbd_destroy_calc(struct cmbd_calc* calc);

struct cmbd_system* cmbd_init_system(
    struct cmbd_calc* calc,
    int n_atoms,
    double* coords,
    double* lattice,
    int* k_grid
);

void cmbd_destroy_system(struct cmbd_system* sys);

struct cmbd_damping* cmbd_init_damping(
    int n_atoms,
    char* version,
    double* R_vdw,
    double* sigma,
    double beta,
    double a
);

void cmbd_destroy_damping(struct cmbd_damping* damping);

double cmbd_ts_energy(
    struct cmbd_system* sys,
    int n_atoms,
    double* alpha_0,
    double* C6,
    struct cmbd_damping* damping,
    double* gradients
);

double cmbd_mbd_energy(
    struct cmbd_system* sys,
    int n_atoms,
    double* alpha_0,
    double* C6,
    struct cmbd_damping* damping,
    double* gradients
);

double cmbd_rpa_energy(
    struct cmbd_system* sys,
    int n_atoms,
    double* alpha_0,
    double* C6,
    struct cmbd_damping* damping,
    double* gradients
);

double cmbd_mbd_rsscs_energy(
    struct cmbd_system* sys,
    int n_atoms,
    double* alpha_0,
    double* C6,
    struct cmbd_damping* damping,
    double* gradients,
    double* eigvals,
    double* eigvecs
);

double cmbd_mbd_scs_energy(
    struct cmbd_system* sys,
    int n_atoms,
    double* alpha_0,
    double* C6,
    struct cmbd_damping* damping,
    double* gradients
);

double cmbd_dipole_matrix(
    struct cmbd_system* sys,
    struct cmbd_damping* damping,
    double* k_point,
    double* dipmat
);

double cmbd_coulomb_energy(
    struct cmbd_system* sys,
    int n_atoms,
    double* q,
    double* m,
    double* w_t,
    char* version,
    double* r_vdw,
    double beta,
    double a,
    double* C
);

double cmbd_dipole_energy(
    struct cmbd_system* sys,
    int n_atoms,
    double* a0,
    double* w,
    double* w_t,
    char* version,
    double* r_vdw,
    double beta,
    double a,
    double* C
);
