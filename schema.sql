
CREATE TABLE employees (
	employee_id SERIAL NOT NULL, 
	first_name VARCHAR(50) NOT NULL, 
	last_name VARCHAR(50) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	department VARCHAR(50) NOT NULL, 
	CONSTRAINT employees_pkey PRIMARY KEY (employee_id), 
	CONSTRAINT employees_email_key UNIQUE NULLS DISTINCT (email)
)



CREATE TABLE expense_categories (
	category_id SERIAL NOT NULL, 
	category_name VARCHAR(100) NOT NULL, 
	description TEXT, 
	CONSTRAINT expense_categories_pkey PRIMARY KEY (category_id)
)



CREATE TABLE pg_stat_statements_info (
	dealloc BIGINT, 
	stats_reset TIMESTAMP WITH TIME ZONE
)



CREATE TABLE pg_stat_statements (
	userid OID, 
	dbid OID, 
	toplevel BOOLEAN, 
	queryid BIGINT, 
	query TEXT, 
	plans BIGINT, 
	total_plan_time DOUBLE PRECISION, 
	min_plan_time DOUBLE PRECISION, 
	max_plan_time DOUBLE PRECISION, 
	mean_plan_time DOUBLE PRECISION, 
	stddev_plan_time DOUBLE PRECISION, 
	calls BIGINT, 
	total_exec_time DOUBLE PRECISION, 
	min_exec_time DOUBLE PRECISION, 
	max_exec_time DOUBLE PRECISION, 
	mean_exec_time DOUBLE PRECISION, 
	stddev_exec_time DOUBLE PRECISION, 
	rows BIGINT, 
	shared_blks_hit BIGINT, 
	shared_blks_read BIGINT, 
	shared_blks_dirtied BIGINT, 
	shared_blks_written BIGINT, 
	local_blks_hit BIGINT, 
	local_blks_read BIGINT, 
	local_blks_dirtied BIGINT, 
	local_blks_written BIGINT, 
	temp_blks_read BIGINT, 
	temp_blks_written BIGINT, 
	blk_read_time DOUBLE PRECISION, 
	blk_write_time DOUBLE PRECISION, 
	temp_blk_read_time DOUBLE PRECISION, 
	temp_blk_write_time DOUBLE PRECISION, 
	wal_records BIGINT, 
	wal_fpi BIGINT, 
	wal_bytes NUMERIC, 
	jit_functions BIGINT, 
	jit_generation_time DOUBLE PRECISION, 
	jit_inlining_count BIGINT, 
	jit_inlining_time DOUBLE PRECISION, 
	jit_optimization_count BIGINT, 
	jit_optimization_time DOUBLE PRECISION, 
	jit_emission_count BIGINT, 
	jit_emission_time DOUBLE PRECISION
)



CREATE TABLE expense_reports (
	report_id SERIAL NOT NULL, 
	employee_id INTEGER NOT NULL, 
	report_month DATE NOT NULL, 
	total_amount NUMERIC(10, 2) DEFAULT 0 NOT NULL, 
	submission_date DATE NOT NULL, 
	approval_status VARCHAR(20) NOT NULL, 
	CONSTRAINT expense_reports_pkey PRIMARY KEY (report_id), 
	CONSTRAINT expense_reports_employee_id_fkey FOREIGN KEY(employee_id) REFERENCES employees (employee_id)
)



CREATE TABLE expenses (
	expense_id SERIAL NOT NULL, 
	report_id INTEGER NOT NULL, 
	expense_date DATE NOT NULL, 
	category_id INTEGER NOT NULL, 
	amount NUMERIC(10, 2) NOT NULL, 
	description TEXT, 
	receipt_url TEXT, 
	CONSTRAINT expenses_pkey PRIMARY KEY (expense_id), 
	CONSTRAINT expenses_category_id_fkey FOREIGN KEY(category_id) REFERENCES expense_categories (category_id), 
	CONSTRAINT expenses_report_id_fkey FOREIGN KEY(report_id) REFERENCES expense_reports (report_id)
)

